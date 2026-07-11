from api import incidents
import logging

from backend.ai.services.offline_queue import offline_queue
from backend.ai.services.supabase_service import supabase

import threading

sync_lock = threading.Lock()

logger = logging.getLogger(__name__)


class SyncService:

    def sync(self):

        with sync_lock:

            incidents = offline_queue.get_all()

            if not incidents:
                logger.info("Offline queue is empty.")
                return

            logger.info(f"Syncing {len(incidents)} offline incident(s)...")

            for incident in incidents:

                data = {
                    "incident_id": incident["id"],
                    "title": incident["summary"],
                    "description": incident["summary"],
                    "service": "offline-monitor",
                    "severity": incident["severity"],
                    "status": incident["status"].upper(),
                    "created_at": incident["queued_at"]
                }

                try:
                    response = (
                        supabase
                        .table("incidents")
                        .upsert(
                            data,
                            on_conflict="incident_id"
                        )
                        .execute()
                    )

                    logger.info(f"Synced: {incident['id']}")

                except Exception as e:
                    logger.error(f"Failed to sync {incident['id']}: {e}")

            offline_queue.clear()

            logger.info("Offline queue cleared.")

sync_service = SyncService()