from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class SocialProvider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    APPLE = "apple"

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: 'PhoneRequest'
    language: 'Language'

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class SocialLoginRequest(BaseModel):
    provider: SocialProvider
    token: str

class VerifyEmailRequest(BaseModel):
    code: str

class ResendVerificationRequest(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class PhoneRequest(BaseModel):
    number: str
    country_code: str