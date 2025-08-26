import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from shared.secrets_manager import get_secret

# --- Email Configuration (Retrieved from Secrets Manager) ---


async def send_email(to_email: str, subject: str, body: str):
    # Retrieve secrets
    smtp_server = get_secret("EMAIL_SMTP_SERVER")
    smtp_port = int(get_secret("EMAIL_SMTP_PORT")) # Port should be an integer
    smtp_username = get_secret("EMAIL_SENDER_EMAIL")
    smtp_password = get_secret("EMAIL_SENDER_PASSWORD")
    msg = MIMEMultipart()
    msg["From"] = smtp_username # Use retrieved username
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server: # Use retrieved server and port
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password) # Use retrieved username and password
            server.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Failed to send email: {e}"
