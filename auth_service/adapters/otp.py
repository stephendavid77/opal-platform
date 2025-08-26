from datetime import datetime, timedelta
from typing import Optional

from auth_service.utils.email_sender import send_email
from auth_service.utils.otp_generator import generate_otp

# --- OTP Configuration (PLACEHOLDERS - MOVE TO CONFIGURATION) ---
OTP_EXPIRE_MINUTES = 5
# -----------------------------------------------------------------

# In a real application, OTPs would be stored in Redis or a similar fast key-value store.
# For this example, we'll simulate it with a dictionary (NOT FOR PRODUCTION).
_otp_store = {}


async def generate_and_send_otp(email: str) -> Optional[str]:
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)

    _otp_store[email] = {"code": otp_code, "expires_at": expires_at}

    subject = "Your OpalSuite OTP Code"
    body = f"Your One-Time Password (OTP) is: {otp_code}. It is valid for {OTP_EXPIRE_MINUTES} minutes."

    success, message = await send_email(email, subject, body)
    if success:
        return otp_code
    else:
        print(f"Failed to send OTP email to {email}: {message}")
        return None


async def verify_otp(email: str, otp_code: str) -> bool:
    stored_otp = _otp_store.get(email)
    if not stored_otp:
        return False

    if stored_otp["code"] == otp_code and stored_otp["expires_at"] > datetime.utcnow():
        del _otp_store[email]  # OTP consumed
        return True
    else:
        return False
