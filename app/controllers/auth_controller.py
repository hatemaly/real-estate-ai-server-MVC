from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.models.auth_models import (
    Token, UserRegisterRequest, UserLoginRequest,
    SocialLoginRequest, VerifyEmailRequest,
    ResendVerificationRequest, ForgotPasswordRequest,
    ResetPasswordRequest, OAuthLoginRequest
)
from app.models.user_models.user import User, Language, UserRole


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    # Register a new user
    # Login using social provider (e.g., Google)
    async def social_login(self, request: SocialLoginRequest) -> Token:
        try:
            if request.provider == "google":
                user_data = await self.auth_service.verify_google_token(request.token)
            else:
                raise HTTPException(status_code=400, detail="Unsupported provider")

            email = user_data.get("email")
            user = await self.auth_service.user_service.get_user_by_email(email)

            if not user:
                user = User(
                    email=email,
                    full_name=user_data.get("name", ""),
                    role=UserRole.USER,
                    language=Language.EN
                )
                await self.auth_service.user_service.create_user(user)

            access_token, refresh_token = await self.auth_service.create_access_token({"sub": email})
            return Token(access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Verify email with verification code
    async def verify_email(self, request: VerifyEmailRequest) -> dict:
        success = await self.auth_service.verify_email(request.code)
        if not success:
            raise HTTPException(status_code=400, detail="Invalid verification code")
        return {"success": True}

    # Resend verification code
    async def resend_verification(self, request: ResendVerificationRequest) -> dict:
        await self.auth_service.resend_verification(request.email)
        return {"success": True}

    # Request password reset link
    async def forgot_password(self, request: ForgotPasswordRequest) -> dict:
        await self.auth_service.forgot_password(request.email)
        return {"success": True}

    # Reset password using reset token
    async def reset_password(self, request: ResetPasswordRequest) -> dict:
        try:
            await self.auth_service.reset_password(request.token, request.new_password)
            return {"success": True}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Email/Password Registration
    async def register(self, request: UserRegisterRequest) -> Token:
        try:
            tokens = await self.auth_service.register_user(request)
            return Token(**tokens)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Email/Password Login
    async def login(self, request: UserLoginRequest) -> Token:
        try:
            tokens = await self.auth_service.login_user(request.email, request.password)
            return Token(**tokens)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    # OAuth Login (e.g., Google, GitHub)
    async def oauth_login(self, request: OAuthLoginRequest) -> Token:
        try:
            tokens = await self.auth_service.oauth_login(request.provider, request.token)
            return Token(**tokens)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))