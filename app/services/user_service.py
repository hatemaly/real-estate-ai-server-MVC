# src/services/user_service.py
# This module contains the UserService class which implements business logic
# for user management operations. It acts as an intermediary between the
# controller layer and the data access layer (repository).

from typing import List, Optional
from app.models.user_models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Service class for managing user-related business logic.
    
    This service provides methods for creating, retrieving, updating, and deleting users,
    as well as specialized operations like user activation and filtering by role.
    It delegates data access operations to the user repository.
    
    Attributes:
        repository: The repository that handles data access operations for users
    """
    def __init__(self, repository: UserRepository):
        """
        Initialize the user service with a repository.
        
        Args:
            repository: The repository that will handle data access operations
        """
        self.repository = repository

    async def create_user(self, user: User) -> User:
        """
        Create a new user.
        
        Args:
            user: The user data to save
            
        Returns:
            User: The created user with assigned ID
        """
        await self.repository.save(user)
        return user

    async def update_user(self, user: User) -> User:
        """
        Update an existing user.
        
        Args:
            user: The user data to update (must include ID)
            
        Returns:
            User: The updated user
            
        Raises:
            Exception: If user with the ID doesn't exist
        """
        await self.repository.update(user)
        return user

    async def delete_user(self, user_id: str) -> None:
        """
        Delete a user by ID.
        
        Args:
            user_id: The ID of the user to delete
            
        Raises:
            Exception: If user with the ID doesn't exist
        """
        await self.repository.delete(user_id)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        print(user_id , " from service \n\n")
        return await self.repository.get_by_id(user_id)

    async def get_users_by_email(self, email: str) -> Optional[User]:
        """
        Get users with a specific email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return await self.repository.get_by_email(email)

    async def get_users_by_role(self, role: str, skip: int = 0, limit: int = 50) -> List[User]:
        """
        Get users with a specific role, with pagination.
        
        Args:
            role: The role to filter by (e.g., 'user', 'admin', 'agent')
            skip: Number of users to skip (for pagination)
            limit: Maximum number of users to return (for pagination)
            
        Returns:
            List[User]: A list of users with the specified role
        """
        return await self.repository.get_users_by_role(role, skip, limit)

    async def get_users_ids_by_role(self, role: str) -> List[str]:
        """
        Get only the IDs of users with a specific role.
        
        This is an optimization for when only the IDs are needed.
        
        Args:
            role: The role to filter by (e.g., 'user', 'admin', 'agent')
            
        Returns:
            List[str]: A list of user IDs with the specified role
        """
        return await self.repository.get_users_ids_by_role(role)

    async def activate_user(self, user_id: str) -> None:
        """
        Activate a user account.
        
        Args:
            user_id: The ID of the user to activate
            
        Raises:
            Exception: If user with the ID doesn't exist
        """
        await self.repository.activate(user_id)

    async def deactivate_user(self, user_id: str) -> None:
        """
        Deactivate a user account.
        
        Args:
            user_id: The ID of the user to deactivate
            
        Raises:
            Exception: If user with the ID doesn't exist
        """
        await self.repository.deactivate(user_id)
