from pydantic import  EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

from app.models.base_model import BaseModelApp


class Token(BaseModelApp):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModelApp):
    email: Optional[str] = None

class SocialProvider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    APPLE = "apple"

class UserRegisterRequest(BaseModelApp):
    email: EmailStr
    password: str
    full_name: str
    phone: 'PhoneRequest'
    language: 'Language'

class UserLoginRequest(BaseModelApp):
    email: EmailStr
    password: str

class SocialLoginRequest(BaseModelApp):
    provider: SocialProvider
    token: str

class VerifyEmailRequest(BaseModelApp):
    code: str

class ResendVerificationRequest(BaseModelApp):
    email: EmailStr

class ForgotPasswordRequest(BaseModelApp):
    email: EmailStr

class ResetPasswordRequest(BaseModelApp):
    token: str
    new_password: str

class PhoneRequest(BaseModelApp):
    number: str
    country_code: str