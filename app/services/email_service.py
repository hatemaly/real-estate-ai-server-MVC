from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings
from fastapi import HTTPException

class EmailService:
    async def send_email(self, email: str, subject: str, html_content: str):
        """General function to send emails"""
        message = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=email,
            subject=subject,
            html_content=html_content)
        await self._send_email(message)

    async def send_verification_email(self, email: str, code: str):
        """Send email verification code"""
        html_content = f"Your verification code is: <strong>{code}</strong>"
        await self.send_email(email, "Email Verification", html_content)

    async def send_password_reset_email(self, email: str, token: str):
        """Send password reset link"""
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        html_content = f"Click here to reset your password: <a href='{reset_link}'>{reset_link}</a>"
        await self.send_email(email, "Password Reset", html_content)

    async def _send_email(self, message: Mail):
        """Helper function to send email using SendGrid"""
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            if response.status_code not in [200, 202]:
                raise HTTPException(status_code=500, detail="Email sending failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
