import logging
from typing import List, Optional
from backend.models.incident import Incident
from backend.database.supabase import supabase_client

logger = logging.getLogger(__name__)

# In-memory backup database to keep the app working if Supabase is not configured yet
mock_incidents_db = []
mock_id_counter = 1

def create_incident(title: str, description: str, severity: str) -> Incident:
    global mock_id_counter
    incident = Incident(
        title=title,
        description=description,
        severity=severity,
        status="open"
    )
    
    if supabase_client:
        try:
            data = incident.to_dict()
            response = supabase_client.table("incidents").insert(data).execute()
            if response.data and len(response.data) > 0:
                return Incident.from_dict(response.data[0])
        except Exception as e:
            logger.error(f"Error creating incident in Supabase: {e}. Saving to in-memory fallback.")
    
    # In-memory fallback
    incident.id = mock_id_counter
    mock_id_counter += 1
    mock_incidents_db.append(incident)
    return incident

def update_incident_status(incident_id: int, status: str) -> Optional[Incident]:
    if supabase_client:
        try:
            response = supabase_client.table("incidents").update({"status": status}).eq("id", incident_id).execute()
            if response.data and len(response.data) > 0:
                return Incident.from_dict(response.data[0])
        except Exception as e:
            logger.error(f"Error updating incident status in Supabase: {e}.")
            
    # In-memory fallback
    for incident in mock_incidents_db:
        if incident.id == incident_id:
            incident.status = status
            return incident
    return None

def update_incident_slack_meta(incident_id: int, channel_id: str, message_ts: str) -> Optional[Incident]:
    if supabase_client:
        try:
            response = supabase_client.table("incidents").update({
                "channel_id": channel_id,
                "message_ts": message_ts
            }).eq("id", incident_id).execute()
            if response.data and len(response.data) > 0:
                return Incident.from_dict(response.data[0])
        except Exception as e:
            logger.error(f"Error updating incident slack meta in Supabase: {e}.")
            
    # In-memory fallback
    for incident in mock_incidents_db:
        if incident.id == incident_id:
            incident.channel_id = channel_id
            incident.message_ts = message_ts
            return incident
    return None

def get_incident(incident_id: int) -> Optional[Incident]:
    if supabase_client:
        try:
            response = supabase_client.table("incidents").select("*").eq("id", incident_id).execute()
            if response.data and len(response.data) > 0:
                return Incident.from_dict(response.data[0])
        except Exception as e:
            logger.error(f"Error fetching incident from Supabase: {e}.")
            
    # In-memory fallback
    for incident in mock_incidents_db:
        if incident.id == incident_id:
            return incident
    return None

def list_incidents() -> List[Incident]:
    if supabase_client:
        try:
            response = supabase_client.table("incidents").select("*").execute()
            if response.data:
                # Supabase table order can be sorted by created_at or id
                sorted_data = sorted(response.data, key=lambda x: x.get("created_at") or "", reverse=True)
                return [Incident.from_dict(item) for item in sorted_data]
        except Exception as e:
            logger.error(f"Error listing incidents from Supabase: {e}.")
            
    # In-memory fallback
    return list(reversed(mock_incidents_db))
