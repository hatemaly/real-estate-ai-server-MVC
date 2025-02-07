from datetime import datetime
from pymongo.collection import Collection
from typing import List, Optional
from app.models.user_models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, collection: Collection):
        super().__init__(collection, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        document = await self.collection.find_one({"email.address": email})
        return User(**document) if document else None

    async def get_by_verification_code(self, code: str) -> Optional[User]:
        document = await self.collection.find_one({"verification_code": code})
        return User(**document) if document else None

    async def verify_email(self, email: str, code: str) -> bool:
        result = await self.collection.update_one(
            {"email.address": email, "verification_code": code},
            {"$set": {"email.is_verified": True}, "$unset": {"verification_code": ""}}
        )
        return result.modified_count > 0

    async def update_verification_code(self, email: str, code: str) -> None:
        await self.collection.update_one(
            {"email.address": email},
            {"$set": {"verification_code": code}}
        )

    async def update_reset_token(self, email: str, token: str, expiry: datetime) -> None:
        await self.collection.update_one(
            {"email.address": email},
            {"$set": {"reset_token": token, "reset_token_expiry": expiry}}
        )

    async def get_by_reset_token(self, token: str) -> Optional[User]:
        document = await self.collection.find_one({"reset_token": token})
        return User(**document) if document else None

    async def update_password(self, email: str, password_hash: str) -> None:
        await self.collection.update_one(
            {"email.address": email},
            {"$set": {"password_hash": password_hash}, "$unset": {"reset_token": "", "reset_token_expiry": ""}}
        )

    async def add_favorite(self, user_id: str, property_id: str) -> None:
        await self.collection.update_one(
            {"_id": user_id},
            {"$addToSet": {"favorites": property_id}}  # $addToSet يضيف فقط إن لم يكن موجودًا
        )

    async def remove_favorite(self, user_id: str, property_id: str) -> None:
        await self.collection.update_one(
            {"_id": user_id},
            {"$pull": {"favorites": property_id}}  # $pull يحذف العنصر إن وُجد
        )
