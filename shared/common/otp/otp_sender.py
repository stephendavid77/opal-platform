from abc import ABC, abstractmethod


class OTPSender(ABC):
    """Abstract base class for OTP senders."""

    @abstractmethod
    async def send_otp(self, recipient: str, otp_code: str, user_id: str):
        """Sends an OTP to the specified recipient."""
        pass
