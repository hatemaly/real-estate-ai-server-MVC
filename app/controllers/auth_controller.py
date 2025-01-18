from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.models.auth_models import Token
from app.models.user_models.user import User, Email, UserRole, Language


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def google_login(self, token: str) -> Token:
        try:
            user_data = await self.auth_service.verify_google_token(token)

            # Check if user exists or create new user
            email = user_data.get("email")
            existing_users = await self.auth_service.user_service.get_users_by_email(email)

            if not existing_users:
                # Create new user
                new_user = User(
                    email=Email(address=email, is_verified=True),
                    full_name=user_data.get("name", ""),
                    role=UserRole.USER,
                    language=Language.EN
                )
                await self.auth_service.user_service.create_user(new_user)

            # Create access token
            access_token = await self.auth_service.create_access_token(
                {"sub": email}
            )
            return Token(access_token=access_token)

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
