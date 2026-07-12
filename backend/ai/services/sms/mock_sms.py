import logging

from .base import BaseSMSProvider

logger = logging.getLogger(__name__)


class MockSMSProvider(BaseSMSProvider):

    def send_sms(self, phone: str, message: str):
        logger.info(f"[Mock SMS] To: {phone} | Message: {message}")

sms_provider = MockSMSProvider()