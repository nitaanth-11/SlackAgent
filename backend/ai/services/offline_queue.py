import json
import os
from datetime import datetime


class OfflineQueue:
    def __init__(self, filename="offline_queue.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def add_incident(self, incident):
        with open(self.filename, "r") as f:
            queue = json.load(f)

        incident["queued_at"] = datetime.now().isoformat()
        incident["status"] = "pending_sync"

        queue.append(incident)

        with open(self.filename, "w") as f:
            json.dump(queue, f, indent=4)

    def get_all(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def clear(self):
        with open(self.filename, "w") as f:
            json.dump([], f)


offline_queue = OfflineQueue()