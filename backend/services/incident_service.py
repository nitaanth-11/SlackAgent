import uuid
import logging
from datetime import datetime, timezone
from typing import Optional

from database.supabase import supabase

logger = logging.getLogger(__name__)


class IncidentService:

    @staticmethod
    def _generate_id() -> str:
        return f"INC-{str(uuid.uuid4())[:8].upper()}"

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    @staticmethod
    def create_incident(data: dict) -> dict:
        incident = {
            "incident_id": IncidentService._generate_id(),
            "title": data["title"],
            "description": data.get("description", ""),
            "service": data.get("service", "unknown"),
            "severity": data.get("severity", "MEDIUM").upper(),
            "status": "OPEN",
            "owner": None,
            "slack_channel": None,
            "slack_message_ts": None,
            "created_at": IncidentService._now(),
            "updated_at": IncidentService._now(),
            "resolved_at": None,
        }

        response = supabase.table("incidents").insert(incident).execute()
        logger.info(f"Incident created: {incident['incident_id']}")
        return response.data[0]

    # --------------------------------------------------
    # Get One
    # --------------------------------------------------

    @staticmethod
    def get_incident(incident_id: str) -> Optional[dict]:
        response = (
            supabase.table("incidents")
            .select("*")
            .eq("incident_id", incident_id)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None

    # --------------------------------------------------
    # List All
    # --------------------------------------------------

    @staticmethod
    def list_incidents() -> list:
        response = (
            supabase.table("incidents")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    @staticmethod
    def update_incident(incident_id: str, updates: dict) -> Optional[dict]:
        updates["updated_at"] = IncidentService._now()

        response = (
            supabase.table("incidents")
            .update(updates)
            .eq("incident_id", incident_id)
            .execute()
        )

        if response.data:
            logger.info(f"Incident updated: {incident_id}")
            return response.data[0]
        return None

    # --------------------------------------------------
    # Assign Owner
    # --------------------------------------------------

    @staticmethod
    def assign_owner(incident_id: str, owner: str) -> Optional[dict]:
        return IncidentService.update_incident(incident_id, {
            "owner": owner,
            "status": "ASSIGNED",
        })

    # --------------------------------------------------
    # Resolve
    # --------------------------------------------------

    @staticmethod
    def resolve_incident(incident_id: str) -> Optional[dict]:
        return IncidentService.update_incident(incident_id, {
            "status": "RESOLVED",
            "resolved_at": IncidentService._now(),
        })

    # --------------------------------------------------
    # Update Slack Metadata
    # --------------------------------------------------

    @staticmethod
    def update_slack_meta(incident_id: str, channel: str, ts: str) -> Optional[dict]:
        return IncidentService.update_incident(incident_id, {
            "slack_channel": channel,
            "slack_message_ts": ts,
        })