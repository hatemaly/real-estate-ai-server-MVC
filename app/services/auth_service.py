from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import httpx
from app.models.user_models.user import User, Email
from app.services.user_service import UserService
from app.config import settings


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def verify_google_token(self, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise ValueError("Failed to verify Google token")
            return response.json()

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

    async def get_current_user(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get("sub")
            if email is None:
                return None
            users = await self.user_service.get_users_by_email(email)
            if users and len(users) > 0:
                return users[0]
        except JWTError:
            return None
        return None