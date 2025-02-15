from fastapi import HTTPException

from app.models.user_models.user import User, UserRole, Language
from datetime import datetime, timedelta
from pymongo.collection import Collection
from typing import List, Optional
from app.models.user_models.user import User, SocialAccount
from app.repositories.base_repository import BaseRepository
from app.models.user_models.user import SocialProvider
import hashlib
import uuid

class UserRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, User)

    # OAuth authentication methods
    async def get_by_provider_and_user_id(self, provider: SocialProvider, provider_user_id: str) -> Optional[User]:
        """Get user by OAuth provider and user ID"""
        document = await self.collection.find_one({"social_providers": provider, f"provider_user_ids.{provider}": provider_user_id})
        return User(**document) if document else None

    async def create_or_update_oauth_user(self, email: str, provider: SocialProvider, provider_user_id: str, first_name: str, last_name: str) -> User:
        """Create or update user with OAuth data"""
        user = await self.get_by_email(email)
        if not user:
            # If no user exists, create a new user
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                social_providers=[provider],
                role=UserRole.USER,
                language=Language.EN
            )
            await self.save(user)

        # Create or update the social account info
        social_account = SocialAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token="",  # Access token management is usually handled elsewhere
            refresh_token=None,
            expires_at=datetime.utcnow(),
            scopes=[]
        )
        await self.collection.update_one(
            {"_id": user.id},
            {"$set": {f"social_providers.{provider}": provider_user_id}}
        )
        return user

    async def create_user(self, user: User) -> User:
        user_id = str(uuid.uuid4())
        user_dict = user.model_dump()
        user_dict["_id"] = user_id
        user_dict["role"] = user.role.value
        user_dict["language"] = user.language.value
        user_dict["created_at"] = user.created_at.isoformat()
        user_dict["updated_at"] = user.updated_at.isoformat()
        try:
            result = await self.collection.insert_one(user_dict)
            inserted_user = await self.collection.find_one({"_id": user_id})
            if not inserted_user:
                raise HTTPException(status_code=500, detail="Failed to retrieve inserted user")

            return User(**inserted_user)

        except Exception as e:
            # 🔥 Log the error
            print(f"🚨 Database Insert Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error: Failed to create user")
        return user

    # Email/Password authentication methods
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        document = await self.collection.find_one({"email": email})
        return User(**document) if document else None

    async def verify_email(self, email: str, code: str) -> bool:
        """Verify user's email using verification code"""
        result = await self.collection.update_one(
            {"email": email, "verification_code": code},
            {"$set": {"is_verified": True}, "$unset": {"verification_code": ""}}
        )
        return result.modified_count > 0

    async def update_verification_code(self, email: str, code: str) -> None:
        """Update email verification code"""
        await self.collection.update_one(
            {"email": email},
            {"$set": {"verification_code": code}}
        )

    async def update_reset_token(self, email: str, token: str, expiry: datetime) -> None:
        """Update password reset token"""
        await self.collection.update_one(
            {"email": email},
            {"$set": {"reset_token": token, "reset_token_expiry": expiry}}
        )

    async def get_by_reset_token(self, token: str) -> Optional[User]:
        """Get user by password reset token"""
        document = await self.collection.find_one({"reset_token": token})
        return User(**document) if document else None

    async def update_password(self, email: str, password_hash: str) -> None:
        """Update user password"""
        await self.collection.update_one(
            {"email": email},
            {"$set": {"hashed_password": password_hash}, "$unset": {"reset_token": "", "reset_token_expiry": ""}}
        )

    async def add_favorite(self, user_id: str, property_id: str) -> None:
        """Add a favorite property for a user"""
        await self.collection.update_one(
            {"_id": user_id},
            {"$addToSet": {"favorites": property_id}}  # $addToSet prevents duplicate entries
        )

    async def remove_favorite(self, user_id: str, property_id: str) -> None:
        """Remove a favorite property for a user"""
        await self.collection.update_one(
            {"_id": user_id},
            {"$pull": {"favorites": property_id}}  # $pull removes the specified item
        )

    # Utility method to compare hashed password
    def verify_password(self, stored_hash: str, password: str) -> bool:
        """Compare hashed password with plain text password"""
        return stored_hash == hashlib.sha256(password.encode()).hexdigest()  # Simplified example

    async def update_user(self, user: User) -> None:
        """Update user information"""
        document = user.dict(by_alias=True)
        await self.collection.replace_one({"_id": user.id}, document)
