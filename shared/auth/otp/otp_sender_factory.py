import os
from typing import Type

from shared.auth.otp.otp_sender import OTPSender
from shared.auth.otp.senders.email.email_sender import EmailOTPSender
from shared.auth.otp.senders.sms.sms_sender import SMSOTPSender
from shared.secrets_manager import get_secret


def get_otp_sender() -> OTPSender:
    """Factory function to get the appropriate OTP sender based on configuration."""
    sender_type = get_secret("OTP_SENDER_TYPE")
    if sender_type is None:
        sender_type = "email"  # Default if not found
    sender_type = sender_type.lower()

    if sender_type == "email":
        return EmailOTPSender()
    elif sender_type == "sms":
        return SMSOTPSender()
    else:
        raise ValueError(f"Unsupported OTP sender type: {sender_type}")
