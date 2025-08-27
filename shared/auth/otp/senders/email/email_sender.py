import smtplib
from email.mime.text import MIMEText

from shared.auth.otp.otp_sender import OTPSender
from shared.secrets_manager import get_secret  # Corrected import


class EmailOTPSender(OTPSender):
    """Concrete implementation for sending OTPs via email."""

    def __init__(self):
        self.smtp_server = get_secret("EMAIL_SMTP_SERVER")
        smtp_port_str = get_secret("EMAIL_SMTP_PORT")
        self.smtp_port = int(smtp_port_str) if smtp_port_str else 587
        self.smtp_username = get_secret(
            "EMAIL_SENDER_EMAIL"
        )  # Assuming username is sender email
        self.smtp_password = get_secret("EMAIL_SENDER_PASSWORD")
        self.sender_email = get_secret("EMAIL_SENDER_EMAIL")

        if not all(
            [
                self.smtp_server,
                self.smtp_username,
                self.smtp_password,
                self.sender_email,
            ]
        ):
            raise ValueError(
                "SMTP environment variables are not fully configured for EmailOTPSender. Please ensure they are set via secrets_manager."
            )

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
            print("--- otp_sender.send_otp() returning True ---")  # Add this
            return True
        except Exception as e:
            print(f"Failed to send OTP to {recipient}: {e}")
            print("--- otp_sender.send_otp() returning False ---")  # Add this
            return False
