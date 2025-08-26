import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Email Configuration (PLACEHOLDERS - MOVE TO CONFIGURATION) ---
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@example.com"
SMTP_PASSWORD = "your_email_password"
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
