# Real Estate AI Application - Architecture & Commenting Rules

## MVC Architecture Overview

This real estate application follows the Model-View-Controller (MVC) pattern adapted for a FastAPI + MongoDB framework:

### Models (M)

- **Purpose**: Represent data structures and database schemas
- **Location**: Organized in dedicated folders by domain (`user_models`, `location_models`, `property_models`, etc.)
- **Responsibilities**:
  - Define data schemas for MongoDB collections
  - Implement data validation rules through Pydantic models
  - Provide serialization/deserialization for API I/O
  - Include simple data-specific business logic

### Views (V)

- **Purpose**: Handle HTTP requests/responses
- **Location**: In the `routers` directory, organized by feature
- **Responsibilities**:
  - Define API endpoints with FastAPI decorators
  - Process request parameters and validate input
  - Call appropriate controllers to execute business logic
  - Format and return API responses
  - Handle API documentation (through FastAPI's automatic docs generation)

### Controllers (C)

- **Purpose**: Implement business logic
- **Location**: In the `controllers` directory, organized by domain
- **Responsibilities**:
  - Coordinate operations between models
  - Implement complex business rules
  - Process data before/after database operations
  - Handle service integrations (e.g., AI/LLM integrations)
  - Provide error handling for business logic

## Project Structure

```
real-estate-ai-server-MVC/
├── main.py                 # Application entry point
├── config/                 # Configuration files
├── models/                 # Domain-specific model folders
│   ├── user_models/        # User-related data models
│   ├── location_models/    # Location-related data models
│   ├── property_models/    # Property-related data models
│   └── ai_models/          # AI-related data models
├── controllers/            # Business logic
│   ├── user_controller.py
│   ├── auth_controller.py
│   ├── property_controller.py
│   └── ai_controller.py
├── routers/                # API routes/endpoints (Views)
│   ├── user_routes.py
│   ├── auth_routes.py
│   ├── property_routes.py
│   └── ai_routes.py
├── services/               # External service integrations
│   ├── db_service.py       # MongoDB connection service
│   ├── ai_service.py       # LLM integration service
│   └── email_service.py    # Email service
├── utils/                  # Utility functions
├── middleware/             # Custom middleware
├── tests/                  # Test files
└── docs/                   # Documentation
```

## Naming Conventions

- **Files**: snake_case (e.g., `user_controller.py`)
- **Classes**: PascalCase (e.g., `UserModel`)
- **Functions/Methods**: snake_case (e.g., `get_user_by_id`)
- **Variables**: snake_case (e.g., `user_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_USERS_PER_PAGE`)
- **MongoDB Collections**: PascalCase, singular (e.g., `User`, `Property`)
- **API Routes**: kebab-case (e.g., `/api/user-profiles`)

## Code Commenting Standards

### File Headers

Every file should include a docstring at the top describing its purpose:

```python
"""
Module Name

Brief description of the module's purpose and functionality.
Additional details if necessary.
"""
```

### Class Documentation

Classes should have descriptive docstrings explaining their purpose:

```python
class ExampleClass:
    """
    Brief description of the class.

    More detailed explanation if necessary.
    Includes information about the class's role in the system.
    """
```

### Function/Method Documentation

Functions and methods should include docstrings with:

- Brief description
- Parameters with types
- Return values with types
- Exceptions that might be raised

```python
def example_function(param1, param2):
    """
    Brief description of what the function does.

    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2

    Returns:
        return_type: Description of the return value

    Raises:
        ExceptionType: When and why this exception might be raised
    """
```

### Inline Comments

- Use inline comments sparingly for non-obvious code
- Explain "why" rather than "what" when possible
- Format as complete sentences with proper punctuation

```python
# This is calculating the weighted average based on user preferences
weighted_score = (price_score * 0.4) + (location_score * 0.6)
```

### TODO/FIXME Comments

Use standardized formats for marking pending work:

```python
# TODO(username): Implement caching for this function
# FIXME(username): This has a performance issue when the dataset is large
```

## MongoDB & Pydantic Models Guidelines

- Use Pydantic models for data validation and serialization
- Include example data in Pydantic Config classes for API documentation
- Use type hints for all model fields
- Implement custom validators where necessary
- Include reasonable default values where appropriate

## AI (LLM) Integration Guidelines

- Clearly document all prompt templates used for LLM communication
- Use consistent input/output formats for AI services
- Include confidence scores with AI-generated responses where applicable
- Implement proper error handling for AI service failures
- Log all significant AI interactions for debugging and improvement

## Error Handling

- Use custom exception classes for domain-specific errors
- Implement consistent error responses in API endpoints
- Include appropriate HTTP status codes
- Provide user-friendly error messages
- Log detailed error information for debugging

## Testing Standards

- Write unit tests for all controllers and services
- Include integration tests for API endpoints
- Use mock objects for external dependencies
- Test both success and error paths
- Aim for high test coverage of business logic

## Security Practices

- Never hardcode sensitive information (use environment variables)
- Implement proper authentication and authorization checks
- Validate all user inputs
- Use HTTPS for all API communications
- Implement rate limiting for public endpoints
