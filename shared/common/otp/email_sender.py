import os
import smtplib
from email.mime.text import MIMEText

from shared.common.otp.otp_sender import OTPSender


class EmailOTPSender(OTPSender):
    """Concrete implementation for sending OTPs via email."""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")

        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.sender_email]):
            raise ValueError("SMTP environment variables are not fully configured for EmailOTPSender.")

    async def send_otp(self, recipient: str, otp_code: str, user_id: str):
        """Sends an OTP to the specified email recipient."""
        subject = "Your One-Time Password (OTP)"
        body = f"Your OTP is: {otp_code}. It is valid for 5 minutes."

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = recipient

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            print(f"OTP sent to {recipient} for user {user_id}")
            return True
        except Exception as e:
            print(f"Failed to send OTP to {recipient}: {e}")
            return False