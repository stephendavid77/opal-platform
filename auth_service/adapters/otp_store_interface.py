from abc import ABC, abstractmethod
from typing import Optional


class OTPStoreInterface(ABC):
    """Abstract base class for an OTP store."""

    @abstractmethod
    async def store_otp(self, email: str, otp_code: str) -> None:
        """Stores an OTP for a given email."""
        pass

    @abstractmethod
    async def verify_otp(self, email: str, otp_code: str) -> bool:
        """Verifies an OTP for a given email."""
        pass
