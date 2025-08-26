from typing import Optional

from auth_service.utils.email_sender import send_email
from auth_service.utils.otp_generator import generate_otp
from .otp_store_interface import OTPStoreInterface
from .redis_otp_store import RedisOTPStore

# --- OTP Configuration (MOVE TO A SECURE CONFIGURATION SYSTEM) ---
OTP_EXPIRE_MINUTES = 10
OTP_STORE = "redis"  # Can be 'redis', 'in_memory', etc.
# -----------------------------------------------------------------

def get_otp_store() -> OTPStoreInterface:
    """Factory function to get the configured OTP store."""
    if OTP_STORE == "redis":
        return RedisOTPStore()
    # Add other store implementations here
    # elif OTP_STORE == "in_memory":
    #     return InMemoryOTPStore()
    else:
        raise ValueError(f"Unknown OTP store: {OTP_STORE}")

otp_store = get_otp_store()


async def generate_and_send_otp(email: str) -> Optional[str]:
    otp_code = generate_otp()
    await otp_store.store_otp(email, otp_code)

    subject = "Your OpalSuite OTP Code"
    body = f"Your One-Time Password (OTP) is: {otp_code}. It is valid for {OTP_EXPIRE_MINUTES} minutes."

    success, message = await send_email(email, subject, body)
    if success:
        return otp_code
    else:
        print(f"Failed to send OTP email to {email}: {message}")
        return None


async def verify_otp(email: str, otp_code: str) -> bool:
    return await otp_store.verify_otp(email, otp_code)
