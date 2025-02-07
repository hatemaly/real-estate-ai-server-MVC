from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings
from fastapi import HTTPException

class EmailService:
    async def send_verification_email(self, email: str, code: str):
        message = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=email,
            subject="Email Verification",
            html_content=f"Your verification code is: <strong>{code}</strong>")
        await self._send_email(message)

    async def send_password_reset_email(self, email: str, token: str):
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        message = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=email,
            subject="Password Reset",
            html_content=f"Click here to reset your password: <a href='{reset_link}'>{reset_link}</a>")
        await self._send_email(message)

    async def _send_email(self, message: Mail):
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            if response.status_code not in [200, 202]:
                raise HTTPException(status_code=500, detail="Email sending failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))