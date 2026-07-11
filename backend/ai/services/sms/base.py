from abc import ABC, abstractmethod


class BaseSMSProvider(ABC):

    @abstractmethod
    def send_sms(self, phone: str, message: str):
        pass