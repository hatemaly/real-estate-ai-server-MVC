# src/models/auth_models.py
from pydantic import EmailStr, BaseModel
from typing import Optional, ForwardRef
from datetime import datetime
from enum import Enum

from app.models.base_model import BaseModelApp
from app.models.user_models.object_values import Language, Phone, Email


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
    first_name: str
    last_name: str
    phone: Phone
    language: Language

class UserLoginRequest(BaseModel):
    email: str
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

class PhoneRequest(BaseModel):
    number: str
    country_code: str

