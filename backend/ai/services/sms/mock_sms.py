import logging

from .base import BaseSMSProvider

logger = logging.getLogger(__name__)


class MockSMSProvider(BaseSMSProvider):

    def send_sms(self, phone: str, message: str):
        print("=" * 50)
        print("📱 MOCK SMS SENT")
        print(f"To      : {phone}")
        print(f"Message : {message}")
        print("=" * 50)

sms_provider = MockSMSProvider()