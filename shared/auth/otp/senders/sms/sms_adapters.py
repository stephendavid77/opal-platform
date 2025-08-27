import logging
import os
from abc import ABC, abstractmethod

import boto3
from twilio.rest import Client

logger = logging.getLogger(__name__)


class SMSAdapter(ABC):
    @abstractmethod
    async def send_sms(self, to: str, body: str) -> str:
        """Sends an SMS message and returns a message ID or SID."""
        pass


class TwilioAdapter(SMSAdapter):
    def __init__(self, account_sid: str, auth_token: str, phone_number: str):
        self.client = Client(account_sid, auth_token)
        self.phone_number = phone_number

    async def send_sms(self, to: str, body: str) -> str:
        try:
            message = self.client.messages.create(
                to=to, from_=self.phone_number, body=body
            )
            logger.info(f"Twilio SMS sent to {to}. SID: {message.sid}")
            return message.sid
        except Exception as e:
            logger.error(f"Twilio SMS failed to send to {to}: {e}")
            raise


class SNSAdapter(SMSAdapter):
    def __init__(
        self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str
    ):
        self.client = boto3.client(
            "sns",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    async def send_sms(self, to: str, body: str) -> str:
        try:
            # For SNS, 'to' should be a phone number in E.164 format
            response = await self.client.publish(PhoneNumber=to, Message=body)
            message_id = response["MessageId"]
            logger.info(f"SNS SMS sent to {to}. MessageId: {message_id}")
            return message_id
        except Exception as e:
            logger.error(f"SNS SMS failed to send to {to}: {e}")
            raise
