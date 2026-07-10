from fastapi import APIRouter, HTTPException

from schemas.incident import IncidentUpdate, IncidentAssign
from services.incident_service import IncidentService

router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"],
)


@router.get("")
def list_incidents():
    """Return all incidents, newest first."""
    return IncidentService.list_incidents()


@router.get("/{incident_id}")
def get_incident(incident_id: str):
    """Return a single incident by incident_id."""
    incident = IncidentService.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")
    return incident


@router.patch("/{incident_id}")
def update_incident(incident_id: str, payload: IncidentUpdate):
    """Update one or more fields on an incident."""
    existing = IncidentService.get_incident(incident_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")

    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update.")

    # Normalize severity to uppercase
    if "severity" in updates:
        updates["severity"] = updates["severity"].upper()
    if "status" in updates:
        updates["status"] = updates["status"].upper()

    updated = IncidentService.update_incident(incident_id, updates)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update incident.")

    # Update Slack message
    from services.slack_service import SlackService
    SlackService.update_incident_message(updated)

    return updated


@router.post("/{incident_id}/assign")
def assign_owner(incident_id: str, payload: IncidentAssign):
    """Assign an owner to an incident."""
    existing = IncidentService.get_incident(incident_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")

    updated = IncidentService.assign_owner(incident_id, payload.owner)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to assign owner.")

    # Update Slack message
    from services.slack_service import SlackService
    SlackService.update_incident_message(updated)

    return updated


@router.post("/{incident_id}/resolve")
def resolve_incident(incident_id: str):
    """Resolve an incident."""
    existing = IncidentService.get_incident(incident_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found.")

    if existing.get("status", "").upper() == "RESOLVED":
        raise HTTPException(status_code=400, detail="Incident is already resolved.")

    updated = IncidentService.resolve_incident(incident_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to resolve incident.")

    # Update Slack message
    from services.slack_service import SlackService
    SlackService.update_incident_message(updated)

    return updated
