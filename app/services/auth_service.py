from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import random
import string
from app.models.auth_models import UserRegisterRequest
from app.models.user_models.user import User, UserRole
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_service: UserService, email_service: EmailService):
        self.user_service = user_service
        self.email_service = email_service

    async def create_access_token(self, data: dict) -> tuple[str, str]:
        """Generate access and refresh tokens"""
        access_exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_exp = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_data = data.copy()
        access_data.update({"exp": access_exp, "type": "access"})
        access_token = jwt.encode(access_data, settings.SECRET_KEY, algorithm="HS256")

        refresh_data = data.copy()
        refresh_data.update({"exp": refresh_exp, "type": "refresh"})
        refresh_token = jwt.encode(refresh_data, settings.SECRET_KEY, algorithm="HS256")

        return access_token, refresh_token

    async def register_user(self, user_data: UserRegisterRequest) -> dict:
        """Register a new user and send email verification"""
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_pwd = pwd_context.hash(user_data.password)
        verification_code = ''.join(random.choices(string.digits, k=6))

        user = User(
            email=user_data.email,
            password_hash=hashed_pwd,
            full_name=user_data.full_name,
            phone=user_data.phone,
            language=user_data.language,
            verification_code=verification_code
        )
        await self.user_service.create_user(user)
        await self.email_service.send_verification_email(user.email, verification_code)

        access_token, refresh_token = await self.create_access_token({"user_id": user.id, "role": user.role})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "language": user.language,
                "role": user.role,
                "is_verified": user.is_verified
            }
        }

    async def login_user(self, email: str, password: str) -> dict:
        """Authenticate user with email and password"""
        user = await self.user_service.get_user_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        if not user.is_verified:
            raise ValueError("Email not verified")

        access_token, refresh_token = await self.create_access_token({"user_id": user.id, "role": user.role})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "language": user.language,
                "role": user.role,
                "is_verified": user.is_verified
            }
        }

    async def verify_email(self, code: str) -> dict:
        """Verify email using code"""
        success = await self.user_service.verify_email(code)
        return {"success": success}

    async def resend_verification(self, email: str) -> dict:
        """Resend email verification code"""
        code = ''.join(random.choices(string.digits, k=6))
        await self.user_service.update_verification_code(email, code)
        await self.email_service.send_verification_email(email, code)
        return {"success": True}

    async def forgot_password(self, email: str) -> dict:
        """Send password reset link"""
        user = await self.user_service.get_user_by_email(email)
        if user:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            expiry = datetime.utcnow() + timedelta(hours=1)
            await self.user_service.update_reset_token(email, token, expiry)
            await self.email_service.send_password_reset_email(email, token)
        return {"success": True}

    async def reset_password(self, token: str, new_password: str) -> dict:
        """Reset user password using reset token"""
        user = await self.user_service.get_user_by_reset_token(token)
        if not user or user.reset_token_expiry < datetime.utcnow():
            raise ValueError("Invalid or expired token")
        hashed_pwd = pwd_context.hash(new_password)
        await self.user_service.update_password(user.email, hashed_pwd)
        return {"success": True}
