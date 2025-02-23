import hashlib
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import random
from typing import Dict, List, Optional
import string
from app.models.auth_models import UserRegisterRequest
from app.models.user_models.object_values import Email, Language
from app.models.user_models.user import User, UserRole, SocialAccount
from app.services.email_service import EmailService
from app.services.user_service import UserService
from app.config import settings
from passlib.context import CryptContext
from supabase import create_client, Client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_service: UserService, email_service: EmailService):
        self.user_service = user_service
        self.email_service = email_service
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

    async def _get_or_create_user(self, supabase_user: Dict) -> User:
        # Check if user exists in MongoDB
        user = await self.user_repo.get_user_by_supabase_id(supabase_user["id"])
        if not user:
            # Create user in MongoDB
            user_data = {
                "email": supabase_user["email"],
                "first_name": supabase_user.get("display_name", "").split(" ")[0],
                "last_name": supabase_user.get("display_name", "").split(" ")[-1],
                "social_providers": [supabase_user.get("provider")],
                "role": UserRole.USER,
                "language": Language.EN,
                "social_accounts": [
                    SocialAccount(
                        provider=supabase_user.get("provider"),
                        provider_user_id=supabase_user["id"],
                        access_token="",  # Supabase handles tokens
                        refresh_token="",
                        expires_at=datetime.utcnow(),
                        scopes=[],
                    )
                ],
                "is_verified": True,  # Supabase handles email verification
            }
            user = await self.user_repo.create_user(user_data)
        return user

    # Email/Password Registration
    async def register_user(self, request: UserRegisterRequest) -> Dict:
        try:
            # Register user in Supabase
            response = self.supabase.auth.sign_up({
                "email": request.email,
                "password": request.password,
            })
            if response.user:
                # Create user in MongoDB
                user = await self._get_or_create_user(response.user)
                return {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
            else:
                raise ValueError("Registration failed")
        except Exception as e:
            raise ValueError(str(e))

    # Email/Password Login
    async def login_user(self, email: str, password: str) -> Dict:
        try:
            # Login via Supabase
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            if response.user:
                # Get or create user in MongoDB
                user = await self._get_or_create_user(response.user)
                return {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                }
            else:
                raise ValueError("Login failed")
        except Exception as e:
            raise ValueError(str(e))

    async def oauth_login(self, provider: str, token: str) -> Dict:
        try:
            # Verify token with Supabase
            response = self.supabase.auth.get_user(token)
            user = response.user

            # Get or create user in MongoDB
            db_user = await self._get_or_create_user(user)
            return {
                "access_token": token,  # Or generate your own token
                "refresh_token": ""  # Supabase handles refresh tokens
            }
        except Exception as e:
            raise ValueError(str(e))

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
        print(user_data.email)
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        print(user_data)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_pwd = hashlib.sha256(user_data.password.encode()).hexdigest()
        verification_code = ''.join(random.choices(string.digits, k=6))

        print(user_data.email, user_data.first_name,hashed_pwd)
        user = User(
            email=user_data.email,
            hashed_password=hashed_pwd,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            language=user_data.language,
            is_verified=True
        )

        created_user = await self.user_service.create_user(user)
        # await self.email_service.send_verification_email(user.email, verification_code)

        access_token, refresh_token = await self.create_access_token({"user_id": user.id, "role": user.role})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": created_user
        }

    async def login_user(self, email: str, password: str) -> dict:
        print(email , password)
        user = await self.user_service.get_user_by_email(email)
        print(user)
        if not user:
            raise ValueError("Invalid credentials")
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
        if user.hashed_password != hashed_pwd:
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
                "first_name": user.first_name,
                "last_name" : user.last_name,
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
