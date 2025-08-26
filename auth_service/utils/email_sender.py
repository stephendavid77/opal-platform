import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Email Configuration (MOVE TO A SECURE CONFIGURATION/SECRET MANAGEMENT SYSTEM) ---
SMTP_SERVER = "smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USERNAME = "your_mailtrap_username"
SMTP_PASSWORD = "your_mailtrap_password"
# -----------------------------------------------------------------


async def send_email(to_email: str, subject: str, body: str):
    """Sends an email using SMTP."""
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Failed to send email: {e}"
