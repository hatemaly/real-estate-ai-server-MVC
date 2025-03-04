# src/controllers/user_controller.py
# This module contains the UserController which implements user management operations.
# It provides a layer of abstraction between the API routes and the user service,
# handling CRUD operations for user accounts in the application.

from typing import List
from app.services.user_service import UserService
from app.models.user_models.user import User


class UserController:
    """
    Controller handling user management operations in the application.
    
    This controller provides methods for creating, retrieving, updating, and deleting 
    user accounts. It acts as an intermediary between the API routes and the user service,
    delegating business logic to the service layer.
    
    Attributes:
        user_service: Service that implements user-related business logic
    """
    def __init__(self, user_service: UserService):
        """
        Initialize the user controller.
        
        Args:
            user_service: The service that implements user-related business logic
        """
        self.user_service = user_service

    async def create_user(self, user: User) -> User:
        """
        Create a new user account.
        
        Args:
            user: User model containing the new user's information
            
        Returns:
            User: The created user with assigned ID
        """
        return await self.user_service.create_user(user)

    async def get_user_by_id(self, user_id: str) -> User:
        """
        Retrieve a user by their unique identifier.
        
        Args:
            user_id: The unique identifier of the user to retrieve
            
        Returns:
            User: The user with the specified ID
            
        Raises:
            Exception: If no user with the given ID exists
        """
        return await self.user_service.get_user_by_id(user_id)

    async def get_users_by_role(self, role: str, skip: int, limit: int) -> List[User]:
        """
        Retrieve users with a specific role, with pagination.
        
        Args:
            role: The role to filter users by (e.g., 'user', 'admin', 'agent')
            skip: Number of users to skip (for pagination)
            limit: Maximum number of users to return (for pagination)
            
        Returns:
            List[User]: A list of users with the specified role
        """
        return await self.user_service.get_users_by_role(role, skip, limit)

    async def update_user(self, user: User) -> User:
        """
        Update an existing user's information.
        
        Args:
            user: User model containing updated information (must include ID)
            
        Returns:
            User: The updated user
            
        Raises:
            Exception: If no user with the given ID exists
        """
        return await self.user_service.update_user(user)

    async def delete_user(self, user_id: str) -> None:
        """
        Delete a user account.
        
        Args:
            user_id: The unique identifier of the user to delete
            
        Raises:
            Exception: If no user with the given ID exists
        """
        await self.user_service.delete_user(user_id)
