import socket
import time


class OfflineDetector:
    def __init__(self):
        self.is_online = True
        self.previous_status = True
        self.last_checked = None

    def check_connection(self, timeout=3):
        """
        Returns True if internet is available.
        """
        self.last_checked = time.time()

        try:
            socket.setdefaulttimeout(timeout)
            socket.create_connection(("8.8.8.8", 53))
            self.is_online = True
        except OSError:
            self.is_online = False

        return self.is_online

    def get_status(self):
        return {
            "online": self.is_online,
            "last_checked": self.last_checked,
        }


offline_detector = OfflineDetector()