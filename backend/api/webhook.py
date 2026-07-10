from fastapi import APIRouter, HTTPException

from schemas.incident import IncidentCreate
from services.incident_service import IncidentService
from services.slack_service import SlackService

router = APIRouter(
    prefix="/api/webhook",
    tags=["Webhook"],
)


@router.post("/alert", status_code=201)
def create_alert(payload: IncidentCreate):
    """Receive an alert and create an incident."""
    try:
        incident = IncidentService.create_incident(payload.model_dump())

        # Post to Slack
        incident = SlackService.post_incident(incident)

        return {
            "status": "created",
            "incident": incident,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
