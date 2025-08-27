import logging

from shared.auth.otp.otp_sender import OTPSender
from shared.auth.otp.senders.sms.sms_adapters import SNSAdapter, TwilioAdapter
from shared.secrets_manager import get_secret

logger = logging.getLogger(__name__)


class SMSOTPSender(OTPSender):
    def __init__(self):
        sms_provider_type = get_secret("SMS_PROVIDER_TYPE")
        if sms_provider_type is None:
            sms_provider_type = "twilio"  # Default if not found
        sms_provider_type = sms_provider_type.lower()

        if sms_provider_type == "twilio":
            self.adapter = TwilioAdapter(
                get_secret("TWILIO_ACCOUNT_SID"),
                get_secret("TWILIO_AUTH_TOKEN"),
                get_secret("TWILIO_PHONE_NUMBER"),
            )
        elif sms_provider_type == "sns":
            self.adapter = SNSAdapter(
                get_secret("AWS_ACCESS_KEY_ID"),
                get_secret("AWS_SECRET_ACCESS_KEY"),
                get_secret("AWS_REGION"),
            )
        else:
            raise ValueError(f"Unsupported SMS provider type: {sms_provider_type}")

    async def send_otp(self, recipient: str, otp_code: str, user_id: int) -> bool:
        try:
            # The actual SMS sending is delegated to the chosen adapter
            message_id = await self.adapter.send_sms(
                recipient, f"Your OTP is: {otp_code}"
            )
            logger.info(
                f"SMS OTP sent to {recipient} for user {user_id}. Message ID: {message_id}"
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to send SMS OTP to {recipient} for user {user_id}: {e}"
            )
            return False
