import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.services.user_service import UserService
from app.models.user_models.user import User, Email, UserRole, Language


@pytest.fixture
def mock_user_repository():
    """Fixture that provides a mocked UserRepository."""
    return AsyncMock()


@pytest.fixture
def user_service(mock_user_repository):
    """Fixture that provides a UserService with a mocked repository."""
    return UserService(mock_user_repository)


class TestUserService:
    """Tests for the UserService class."""

    @pytest.mark.asyncio
    async def test_create_user(self, user_service, mock_user_repository):
        """Test creating a new user."""
        # Arrange
        test_user = User(
            email=Email(address="test@example.com", is_verified=False),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        mock_user_repository.create_user.return_value = test_user
        
        # Act
        result = await user_service.create_user(test_user)
        
        # Assert
        assert result == test_user
        mock_user_repository.create_user.assert_called_once_with(test_user)

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user_service, mock_user_repository):
        """Test retrieving a user by ID."""
        # Arrange
        test_user_id = "12345"
        test_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        mock_user_repository.get_user_by_id.return_value = test_user
        
        # Act
        result = await user_service.get_user_by_id(test_user_id)
        
        # Assert
        assert result == test_user
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, user_service, mock_user_repository):
        """Test retrieving a non-existent user by ID."""
        # Arrange
        test_user_id = "non_existent_id"
        mock_user_repository.get_user_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.get_user_by_id(test_user_id)
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)

    @pytest.mark.asyncio
    async def test_get_users_by_email(self, user_service, mock_user_repository):
        """Test retrieving users by email."""
        # Arrange
        test_email = "test@example.com"
        test_user = User(
            email=Email(address=test_email, is_verified=True),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        mock_user_repository.get_users_by_email.return_value = [test_user]
        
        # Act
        result = await user_service.get_users_by_email(test_email)
        
        # Assert
        assert len(result) == 1
        assert result[0] == test_user
        mock_user_repository.get_users_by_email.assert_called_once_with(test_email)

    @pytest.mark.asyncio
    async def test_update_user(self, user_service, mock_user_repository):
        """Test updating a user's information."""
        # Arrange
        test_user_id = "12345"
        original_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        
        updated_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Updated Name",
            role=UserRole.USER,
            language=Language.FR  # Changed language
        )
        
        mock_user_repository.get_user_by_id.return_value = original_user
        mock_user_repository.update_user.return_value = updated_user
        
        # Act
        result = await user_service.update_user(test_user_id, updated_user)
        
        # Assert
        assert result == updated_user
        assert result.full_name == "Updated Name"
        assert result.language == Language.FR
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)
        mock_user_repository.update_user.assert_called_once_with(test_user_id, updated_user)

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_service, mock_user_repository):
        """Test updating a non-existent user."""
        # Arrange
        test_user_id = "non_existent_id"
        update_data = User(
            full_name="New Name",
            language=Language.FR
        )
        mock_user_repository.get_user_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.update_user(test_user_id, update_data)
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)
        mock_user_repository.update_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_user(self, user_service, mock_user_repository):
        """Test deleting a user."""
        # Arrange
        test_user_id = "12345"
        test_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        mock_user_repository.get_user_by_id.return_value = test_user
        mock_user_repository.delete_user.return_value = True
        
        # Act
        result = await user_service.delete_user(test_user_id)
        
        # Assert
        assert result is True
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)
        mock_user_repository.delete_user.assert_called_once_with(test_user_id)

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_service, mock_user_repository):
        """Test deleting a non-existent user."""
        # Arrange
        test_user_id = "non_existent_id"
        mock_user_repository.get_user_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await user_service.delete_user(test_user_id)
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)
        mock_user_repository.delete_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_verify_user_email(self, user_service, mock_user_repository):
        """Test verifying a user's email."""
        # Arrange
        test_user_id = "12345"
        test_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=False),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        
        verified_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        
        mock_user_repository.get_user_by_id.return_value = test_user
        mock_user_repository.update_user.return_value = verified_user
        
        # Act
        result = await user_service.verify_email(test_user_id)
        
        # Assert
        assert result == verified_user
        assert result.email.is_verified is True
        mock_user_repository.get_user_by_id.assert_called_once_with(test_user_id)
        # Verify the updated user has a verified email
        updated_user = mock_user_repository.update_user.call_args[0][1]
        assert updated_user.email.is_verified is True 