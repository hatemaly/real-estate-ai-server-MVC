# Authentication and User Testing Guide

This document provides instructions for running tests related to authentication and user functionality in the real-estate-ai-server-MVC project.

## Setup

1. Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

2. Ensure you have pytest installed:

```bash
pip install pytest pytest-asyncio pytest-cov
```

## Test Structure

The tests are organized as follows:

- `test_auth.py` - Tests for authentication controller and service
- `test_auth_router.py` - Tests for authentication API endpoints
- `test_user.py` - Tests for user service functionality
- `test_user_router.py` - Tests for user API endpoints

## Running Tests

### Running All Tests

To run all tests:

```bash
pytest
```

### Running Specific Test Files

To run a specific test file:

```bash
pytest tests/test_auth.py
pytest tests/test_user.py
```

### Running Tests With a Specific Marker

Tests are marked as unit, integration, or e2e:

```bash
pytest -m unit
pytest -m integration
```

### Running Tests With Coverage

To run tests and generate a coverage report:

```bash
pytest --cov=app tests/
```

For a detailed HTML coverage report:

```bash
pytest --cov=app --cov-report=html tests/
```

## Test Types

### Unit Tests

These test individual components in isolation using mocks.

### Integration Tests

These test the interaction between components, with some mocked dependencies.

### End-to-End Tests

These test the full system, with minimal mocking.

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Place tests in the appropriate test file based on the component being tested
2. Use descriptive test names that clearly indicate what is being tested
3. Follow the Arrange-Act-Assert pattern in test methods
4. Use appropriate markers (unit, integration, e2e)
5. Mock external dependencies as needed

## Test Environment

The tests use a fixture-based approach to provide test resources. Common fixtures include:

- `mock_auth_service` - Provides a mocked AuthService
- `mock_user_repository` - Provides a mocked UserRepository
- `auth_controller` - Provides an AuthController with mocked dependencies
- `user_service` - Provides a UserService with mocked dependencies
- `test_app` - Provides a FastAPI test application
- `client` - Provides a FastAPI TestClient for making requests

## Troubleshooting

If you encounter issues with the tests:

1. Ensure all dependencies are installed
2. Check that you're running the tests from the project root directory
3. Verify that pytest.ini is correctly configured
4. Look for any import errors, which may indicate missing dependencies

For more help, please refer to the pytest documentation: https://docs.pytest.org/
