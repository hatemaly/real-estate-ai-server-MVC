import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.auth_router import router, get_auth_controller
from app.controllers.auth_controller import AuthController
from app.models.auth_models import Token


@pytest.fixture
def mock_auth_controller():
    """Fixture that provides a mocked AuthController."""
    controller = AsyncMock(spec=AuthController)
    return controller


@pytest.fixture
def test_app(mock_auth_controller):
    """Fixture that provides a FastAPI test application with the auth router."""
    app = FastAPI()
    
    # Override the dependency to return our mocked controller
    async def override_get_auth_controller():
        return mock_auth_controller
    
    app.include_router(router)
    app.dependency_overrides[get_auth_controller] = override_get_auth_controller
    
    return app


@pytest.fixture
def client(test_app):
    """Fixture that provides a test client for making requests."""
    return TestClient(test_app)


class TestAuthRouter:
    """Tests for the authentication router endpoints."""
    
    @pytest.mark.asyncio
    async def test_google_login_success(self, client, mock_auth_controller):
        """Test successful Google login."""
        # Arrange
        test_token = "valid_google_token"
        mock_access_token = "app_access_token"
        
        # Configure mock to return a token when google_login is called
        mock_auth_controller.google_login.return_value = Token(access_token=mock_access_token)
        
        # Act
        response = client.post("/login/google", params={"token": test_token})
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"access_token": mock_access_token}
        mock_auth_controller.google_login.assert_awaited_once_with(test_token)
    
    @pytest.mark.asyncio
    async def test_google_login_invalid_token(self, client, mock_auth_controller):
        """Test Google login with an invalid token."""
        # Arrange
        test_token = "invalid_google_token"
        error_message = "Invalid token"
        
        # Configure mock to raise an exception when google_login is called
        from fastapi import HTTPException
        mock_auth_controller.google_login.side_effect = HTTPException(
            status_code=400, detail=error_message
        )
        
        # Act
        response = client.post("/login/google", params={"token": test_token})
        
        # Assert
        assert response.status_code == 400
        assert error_message in response.json()["detail"]
        mock_auth_controller.google_login.assert_awaited_once_with(test_token)


# Integration tests with full request flow
@pytest.mark.integration
class TestAuthIntegration:
    """Integration tests for the authentication flow."""
    
    @pytest.mark.asyncio
    @patch("app.routers.auth_router.get_auth_controller")
    async def test_google_login_full_flow(self, mock_get_controller):
        """Test the complete Google login flow."""
        # This test would use a real FastAPI app with mocked dependencies
        # to test the complete flow from router to controller to service
        
        # Arrange
        test_token = "valid_google_token"
        mock_access_token = "app_access_token"
        
        mock_controller = AsyncMock()
        mock_controller.google_login.return_value = Token(access_token=mock_access_token)
        mock_get_controller.return_value = mock_controller
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        # Act
        response = client.post("/login/google", params={"token": test_token})
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"access_token": mock_access_token}
        # Since this is an integration test, we can't easily check if the controller method was called
        # However, we can check the return value of the endpoint matches what we'd expect 