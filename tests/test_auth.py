import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.models.auth_models import Token
from app.models.user_models.user import User, Email, UserRole, Language


@pytest.fixture
def mock_auth_service():
    """Fixture that provides a mocked AuthService."""
    auth_service = AsyncMock(spec=AuthService)
    auth_service.user_service = AsyncMock()
    return auth_service


@pytest.fixture
def auth_controller(mock_auth_service):
    """Fixture that provides an AuthController with a mocked AuthService."""
    return AuthController(mock_auth_service)


class TestAuthController:
    """Tests for the AuthController class."""

    @pytest.mark.asyncio
    async def test_google_login_existing_user(self, auth_controller, mock_auth_service):
        """Test successful Google login for an existing user."""
        # Arrange
        test_email = "test@example.com"
        test_name = "Test User"
        mock_token = "google_oauth_token"
        mock_user_data = {"email": test_email, "name": test_name}
        mock_access_token = "app_access_token"
        
        # Configure mocks
        mock_auth_service.verify_google_token.return_value = mock_user_data
        mock_auth_service.user_service.get_users_by_email.return_value = [
            User(
                email=Email(address=test_email, is_verified=True),
                full_name=test_name,
                role=UserRole.USER,
                language=Language.EN
            )
        ]
        mock_auth_service.create_access_token.return_value = mock_access_token
        
        # Act
        result = await auth_controller.google_login(mock_token)
        
        # Assert
        assert isinstance(result, Token)
        assert result.access_token == mock_access_token
        mock_auth_service.verify_google_token.assert_called_once_with(mock_token)
        mock_auth_service.user_service.get_users_by_email.assert_called_once_with(test_email)
        mock_auth_service.create_access_token.assert_called_once_with({"sub": test_email})
        # Ensure user creation was not called for existing user
        mock_auth_service.user_service.create_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_google_login_new_user(self, auth_controller, mock_auth_service):
        """Test successful Google login for a new user."""
        # Arrange
        test_email = "new_user@example.com"
        test_name = "New User"
        mock_token = "google_oauth_token"
        mock_user_data = {"email": test_email, "name": test_name}
        mock_access_token = "app_access_token"
        
        # Configure mocks
        mock_auth_service.verify_google_token.return_value = mock_user_data
        mock_auth_service.user_service.get_users_by_email.return_value = []  # No existing user
        mock_auth_service.create_access_token.return_value = mock_access_token
        
        # Act
        result = await auth_controller.google_login(mock_token)
        
        # Assert
        assert isinstance(result, Token)
        assert result.access_token == mock_access_token
        mock_auth_service.verify_google_token.assert_called_once_with(mock_token)
        mock_auth_service.user_service.get_users_by_email.assert_called_once_with(test_email)
        
        # Verify user creation was called with correct parameters
        mock_auth_service.user_service.create_user.assert_called_once()
        created_user = mock_auth_service.user_service.create_user.call_args[0][0]
        assert created_user.email.address == test_email
        assert created_user.email.is_verified is True
        assert created_user.full_name == test_name
        assert created_user.role == UserRole.USER
        assert created_user.language == Language.EN
        
        mock_auth_service.create_access_token.assert_called_once_with({"sub": test_email})

    @pytest.mark.asyncio
    async def test_google_login_error(self, auth_controller, mock_auth_service):
        """Test Google login with an authentication error."""
        # Arrange
        mock_token = "invalid_token"
        mock_auth_service.verify_google_token.side_effect = Exception("Invalid token")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_controller.google_login(mock_token)
        
        assert exc_info.value.status_code == 400
        assert "Invalid token" in str(exc_info.value.detail)
        mock_auth_service.verify_google_token.assert_called_once_with(mock_token)


class TestAuthService:
    """Tests for the AuthService class."""
    
    @pytest.fixture
    def mock_user_service(self):
        """Fixture that provides a mocked UserService for auth service tests."""
        return AsyncMock()

    @pytest.fixture
    def auth_service(self, mock_user_service):
        """Fixture that provides an AuthService with mocked dependencies."""
        return AuthService(mock_user_service)
    
    @pytest.mark.asyncio
    @patch('app.services.auth_service.jwt')
    @patch('app.services.auth_service.datetime')
    async def test_create_access_token(self, mock_datetime, mock_jwt, auth_service):
        """Test creating an access token."""
        # Arrange
        data = {"sub": "test@example.com"}
        mock_now = MagicMock()
        mock_datetime.utcnow.return_value = mock_now
        mock_expires = MagicMock()
        mock_now + mock_datetime.timedelta.return_value = mock_expires
        
        # Configure environment variables for testing
        with patch('app.services.auth_service.settings') as mock_settings:
            mock_settings.SECRET_KEY = "test_secret_key"
            mock_settings.ALGORITHM = "HS256"
            mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
            
            # Act
            await auth_service.create_access_token(data)
            
            # Assert
            mock_datetime.utcnow.assert_called_once()
            mock_datetime.timedelta.assert_called_once_with(minutes=30)
            mock_jwt.encode.assert_called_once()
            # Verify the token data includes expiration time
            encoded_data = mock_jwt.encode.call_args[0][0]
            assert encoded_data["sub"] == "test@example.com"
            assert "exp" in encoded_data

    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_verify_google_token_valid(self, mock_async_client, auth_service):
        """Test verifying a valid Google token."""
        # Arrange
        mock_token = "valid_google_token"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "test@example.com",
            "name": "Test User",
            "email_verified": True
        }
        
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response
        mock_async_client.return_value = mock_client
        
        # Act
        result = await auth_service.verify_google_token(mock_token)
        
        # Assert
        assert result["email"] == "test@example.com"
        assert result["name"] == "Test User"
        mock_client.get.assert_called_once()
        
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_verify_google_token_invalid(self, mock_async_client, auth_service):
        """Test verifying an invalid Google token."""
        # Arrange
        mock_token = "invalid_google_token"
        mock_response = MagicMock()
        mock_response.status_code = 401
        
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response
        mock_async_client.return_value = mock_client
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await auth_service.verify_google_token(mock_token)
        
        assert "Google token verification failed" in str(exc_info.value)
        mock_client.get.assert_called_once() 