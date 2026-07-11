import json
from pathlib import Path

CACHE_FILE = Path("location_cache.json")


class LocationCache:
    def save(self, latitude, longitude):
        with open(CACHE_FILE, "w") as f:
            json.dump(
                {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                f,
                indent=4,
            )

    def get(self):
        if not CACHE_FILE.exists():
            return None

        with open(CACHE_FILE) as f:
            return json.load(f)


location_cache = LocationCache()