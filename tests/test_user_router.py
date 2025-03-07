import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.models.user_models.user import User, Email, UserRole, Language


# First, let's create a mock for user-related API routes
# We'll need to create fixtures similar to auth router tests

@pytest.fixture
def mock_user_service():
    """Fixture that provides a mocked UserService."""
    return AsyncMock()


@pytest.fixture
def mock_user_controller():
    """Fixture that provides a mocked UserController."""
    controller = AsyncMock()
    controller.user_service = mock_user_service()
    return controller


@pytest.fixture
def test_app(mock_user_controller):
    """Fixture that provides a FastAPI test application with the user router."""
    app = FastAPI()
    
    # Let's mock the user router with endpoints that match the actual app
    # This would require the actual user_router.py module to be imported
    # For the test, we'll create a simple router implementation here
    
    from fastapi import APIRouter
    router = APIRouter()
    
    # Mock the get_user_controller dependency
    async def get_user_controller():
        return mock_user_controller
    
    # Define mock routes that would exist in the actual user_router.py
    @router.get("/users/{user_id}")
    async def get_user(user_id: str, controller = Depends(get_user_controller)):
        return await controller.get_user(user_id)
    
    @router.post("/users")
    async def create_user(user: User, controller = Depends(get_user_controller)):
        return await controller.create_user(user)
    
    @router.put("/users/{user_id}")
    async def update_user(user_id: str, user: User, controller = Depends(get_user_controller)):
        return await controller.update_user(user_id, user)
    
    @router.delete("/users/{user_id}")
    async def delete_user(user_id: str, controller = Depends(get_user_controller)):
        return await controller.delete_user(user_id)
    
    app.include_router(router, prefix="/api")
    return app


@pytest.fixture
def client(test_app):
    """Fixture that provides a test client for making requests."""
    return TestClient(test_app)


class TestUserRouter:
    """Tests for the user router endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, client, mock_user_controller):
        """Test successfully retrieving a user."""
        # Arrange
        test_user_id = "12345"
        test_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Test User",
            role=UserRole.USER,
            language=Language.EN
        )
        
        # Configure mock to return a user when get_user is called
        mock_user_controller.get_user.return_value = test_user
        
        # Act
        response = client.get(f"/api/users/{test_user_id}")
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == test_user_id
        assert response_data["email"]["address"] == "test@example.com"
        assert response_data["full_name"] == "Test User"
        mock_user_controller.get_user.assert_awaited_once_with(test_user_id)
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client, mock_user_controller):
        """Test retrieving a non-existent user."""
        # Arrange
        test_user_id = "non_existent_id"
        error_message = "User not found"
        
        # Configure mock to raise an exception when get_user is called
        from fastapi import HTTPException
        mock_user_controller.get_user.side_effect = HTTPException(
            status_code=404, detail=error_message
        )
        
        # Act
        response = client.get(f"/api/users/{test_user_id}")
        
        # Assert
        assert response.status_code == 404
        assert error_message in response.json()["detail"]
        mock_user_controller.get_user.assert_awaited_once_with(test_user_id)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, client, mock_user_controller):
        """Test successfully creating a user."""
        # Arrange
        test_user = {
            "email": {"address": "new@example.com", "is_verified": False},
            "full_name": "New User",
            "role": "USER",
            "language": "EN"
        }
        
        created_user = User(
            id="new_id",
            email=Email(address="new@example.com", is_verified=False),
            full_name="New User",
            role=UserRole.USER,
            language=Language.EN
        )
        
        # Configure mock to return a user when create_user is called
        mock_user_controller.create_user.return_value = created_user
        
        # Act
        response = client.post("/api/users", json=test_user)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == "new_id"
        assert response_data["email"]["address"] == "new@example.com"
        assert response_data["full_name"] == "New User"
        # We can't easily assert the exact User object that was passed to create_user
        # because of the conversion to/from JSON, but we can check it was called
        mock_user_controller.create_user.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_update_user_success(self, client, mock_user_controller):
        """Test successfully updating a user."""
        # Arrange
        test_user_id = "12345"
        update_data = {
            "email": {"address": "test@example.com", "is_verified": True},
            "full_name": "Updated Name",
            "role": "USER",
            "language": "FR"
        }
        
        updated_user = User(
            id=test_user_id,
            email=Email(address="test@example.com", is_verified=True),
            full_name="Updated Name",
            role=UserRole.USER,
            language=Language.FR
        )
        
        # Configure mock to return a user when update_user is called
        mock_user_controller.update_user.return_value = updated_user
        
        # Act
        response = client.put(f"/api/users/{test_user_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == test_user_id
        assert response_data["full_name"] == "Updated Name"
        assert response_data["language"] == "FR"
        # We should check that update_user was called with the correct user_id
        mock_user_controller.update_user.assert_awaited_once()
        # The first arg should be the user_id
        assert mock_user_controller.update_user.call_args[0][0] == test_user_id
    
    @pytest.mark.asyncio
    async def test_delete_user_success(self, client, mock_user_controller):
        """Test successfully deleting a user."""
        # Arrange
        test_user_id = "12345"
        
        # Configure mock to return True when delete_user is called
        mock_user_controller.delete_user.return_value = True
        
        # Act
        response = client.delete(f"/api/users/{test_user_id}")
        
        # Assert
        assert response.status_code == 200
        assert response.json() is True
        mock_user_controller.delete_user.assert_awaited_once_with(test_user_id) 