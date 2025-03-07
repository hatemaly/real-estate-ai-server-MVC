"""
This module contains pytest fixtures that are available to all test modules.
"""

import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add the root directory to the Python path so imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules after path is set up
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.controllers.auth_controller import AuthController
from app.models.user_models.user import User, Email, UserRole, Language
from app.models.auth_models import Token


@pytest.fixture
def mock_user_repository():
    """Fixture that provides a mocked UserRepository."""
    repository = AsyncMock()
    return repository


@pytest.fixture
def mock_user_service():
    """Fixture that provides a mocked UserService."""
    service = AsyncMock(spec=UserService)
    return service


@pytest.fixture
def user_service(mock_user_repository):
    """Fixture that provides a UserService with a mocked repository."""
    return UserService(mock_user_repository)


@pytest.fixture
def mock_auth_service():
    """Fixture that provides a mocked AuthService."""
    auth_service = AsyncMock(spec=AuthService)
    auth_service.user_service = mock_user_service()
    return auth_service


@pytest.fixture
def auth_service(mock_user_service):
    """Fixture that provides an AuthService with a mocked UserService."""
    return AuthService(mock_user_service)


@pytest.fixture
def auth_controller(mock_auth_service):
    """Fixture that provides an AuthController with a mocked AuthService."""
    return AuthController(mock_auth_service)


@pytest.fixture
def test_app():
    """Fixture that provides a FastAPI test application."""
    app = FastAPI()
    return app


@pytest.fixture
def client(test_app):
    """Fixture that provides a test client for making requests."""
    return TestClient(test_app)


# Sample test data fixtures

@pytest.fixture
def sample_user():
    """Fixture that provides a sample user for testing."""
    return User(
        id="test123",
        email=Email(address="test@example.com", is_verified=True),
        full_name="Test User",
        role=UserRole.USER,
        language=Language.EN
    )


@pytest.fixture
def sample_token():
    """Fixture that provides a sample token for testing."""
    return Token(access_token="sample_access_token") 