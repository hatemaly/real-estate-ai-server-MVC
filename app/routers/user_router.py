# app/routers/user_router.py
# This module defines the FastAPI router for user-related API endpoints.
# It sets up routes for CRUD operations on user resources and configures
# the dependency injection for the user controller.

from fastapi import APIRouter, Depends
from typing import List
from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.database.collections import get_user_collection
from app.services.user_service import UserService
from app.models.user_models.user import User

# Create an API router for user endpoints
router = APIRouter()

async def get_user_controller() -> UserController:
    """
    Dependency injection function to create and provide a UserController instance.
    
    This function follows the repository pattern, creating the entire dependency chain:
    database collection -> repository -> service -> controller
    
    Returns:
        UserController: A configured controller for handling user operations
    """
    user_collection = await get_user_collection()
    repository = UserRepository(user_collection)
    service = UserService(repository)
    return UserController(service)

@router.post("/", response_model=User)
async def create_user(user: User, controller: UserController = Depends(get_user_controller)):
    """
    Create a new user.
    
    Args:
        user: User data from request body
        controller: UserController instance (injected dependency)
    
    Returns:
        User: The created user with assigned ID
    """
    return await controller.create_user(user)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, controller: UserController = Depends(get_user_controller)):
    """
    Get a user by their ID.
    
    Args:
        user_id: The unique identifier of the user to retrieve
        controller: UserController instance (injected dependency)
    
    Returns:
        User: The user with the specified ID
        
    Raises:
        HTTPException: If no user with the given ID exists
    """
    print(user_id , "\n\n")
    return await controller.get_user_by_id(user_id)

@router.get("/", response_model=List[User])
async def get_users_by_role(
    role: str, skip: int = 0, limit: int = 10, controller: UserController = Depends(get_user_controller)
):
    """
    Get a list of users with a specific role, with pagination.
    
    Args:
        role: The role to filter users by (e.g., 'user', 'admin', 'agent')
        skip: Number of users to skip (for pagination)
        limit: Maximum number of users to return (for pagination)
        controller: UserController instance (injected dependency)
    
    Returns:
        List[User]: A list of users with the specified role
    """
    return await controller.get_users_by_role(role, skip, limit)

@router.put("/", response_model=User)
async def update_user(user: User, controller: UserController = Depends(get_user_controller)):
    """
    Update an existing user.
    
    Args:
        user: Updated user data from request body (must include ID)
        controller: UserController instance (injected dependency)
    
    Returns:
        User: The updated user
        
    Raises:
        HTTPException: If no user with the given ID exists
    """
    return await controller.update_user(user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, controller: UserController = Depends(get_user_controller)):
    """
    Delete a user by their ID.
    
    Args:
        user_id: The unique identifier of the user to delete
        controller: UserController instance (injected dependency)
    
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If no user with the given ID exists
    """
    await controller.delete_user(user_id)
    return {"message": "User deleted successfully"}
