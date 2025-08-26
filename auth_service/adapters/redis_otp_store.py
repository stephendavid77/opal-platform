from datetime import datetime, timedelta
import redis
import json
from typing import Optional

from .otp_store_interface import OTPStoreInterface

# --- OTP Configuration (MOVE TO A SECURE CONFIGURATION SYSTEM) ---
OTP_EXPIRE_MINUTES = 10
REDIS_HOST = "localhost"
REDIS_PORT = 6379
# -----------------------------------------------------------------

class RedisOTPStore(OTPStoreInterface):
    """An OTP store that uses Redis as a backend."""

    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db: int = 0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    async def store_otp(self, email: str, otp_code: str) -> None:
        expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
        otp_data = {"code": otp_code, "expires_at": expires_at.isoformat()}
        self.redis_client.setex(
            f"otp:{email}",
            timedelta(minutes=OTP_EXPIRE_MINUTES),
            json.dumps(otp_data),
        )

    async def verify_otp(self, email: str, otp_code: str) -> bool:
        stored_otp_data = self.redis_client.get(f"otp:{email}")
        if not stored_otp_data:
            return False

        stored_otp = json.loads(stored_otp_data)
        expires_at = datetime.fromisoformat(stored_otp["expires_at"])

        if stored_otp["code"] == otp_code and expires_at > datetime.utcnow():
            self.redis_client.delete(f"otp:{email}")  # OTP consumed
            return True
        else:
            return False
