from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import httpx
from passlib.context import CryptContext
import random
import string

from app.models.auth_models import UserRegisterRequest
from app.models.user_models.user import User, Email, UserRole, Language
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_service: UserService, email_service: EmailService):
        self.user_service = user_service
        self.email_service = email_service

    async def verify_google_token(self, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise ValueError("Invalid Google token")
            return response.json()

    async def create_access_token(self, data: dict) -> tuple[str, str]:
        access_exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_exp = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_data = data.copy()
        access_data.update({"exp": access_exp, "type": "access"})
        access_token = jwt.encode(access_data, settings.SECRET_KEY, algorithm="HS256")

        refresh_data = data.copy()
        refresh_data.update({"exp": refresh_exp, "type": "refresh"})
        refresh_token = jwt.encode(refresh_data, settings.SECRET_KEY, algorithm="HS256")

        return access_token, refresh_token

    async def register_user(self, user_data: UserRegisterRequest) -> User:
        existing_user = await self.user_service.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_pwd = pwd_context.hash(user_data.password)
        verification_code = ''.join(random.choices(string.digits, k=6))

        user = User(
            email=Email(address=user_data.email, is_verified=False),
            password_hash=hashed_pwd,
            full_name=user_data.full_name,
            phone=user_data.phone,
            language=user_data.language,
            verification_code=verification_code
        )
        await self.user_service.create_user(user)
        await self._send_verification_email(user.email.address, verification_code)
        return user

    async def login_user(self, email: str, password: str) -> User:
        user = await self.user_service.get_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        if not user.email.is_verified:
            raise ValueError("Email not verified")
        return user

    async def verify_email(self, code: str) -> bool:
        return await self.user_service.verify_email(code)

    async def resend_verification(self, email: str) -> None:
        code = ''.join(random.choices(string.digits, k=6))
        await self.user_service.update_verification_code(email, code)
        await self._send_verification_email(email, code)

    async def forgot_password(self, email: str) -> None:
        user = await self.user_service.get_by_email(email)
        if user:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            expiry = datetime.utcnow() + timedelta(hours=1)
            await self.user_service.update_reset_token(email, token, expiry)
            await self._send_password_reset_email(email, token)

    async def reset_password(self, token: str, new_password: str) -> None:
        user = await self.user_service.get_by_reset_token(token)
        if not user or user.reset_token_expiry < datetime.utcnow():
            raise ValueError("Invalid or expired token")
        hashed_pwd = pwd_context.hash(new_password)
        await self.user_service.update_password(user.email.address, hashed_pwd)

    async def _send_verification_email(self, email: str, code: str):
        await self.email_service.send_verification_email(email, code)

    async def _send_password_reset_email(self, email: str, token: str):
        await self.email_service.send_password_reset_email(email, token)