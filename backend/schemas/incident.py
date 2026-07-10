from pydantic import BaseModel
from typing import Optional


class IncidentCreate(BaseModel):
    title: str
    description: str
    service: str
    severity: str = "medium"


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    service: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None


class IncidentAssign(BaseModel):
    owner: str


class IncidentResponse(BaseModel):
    incident_id: str
    title: str
    description: str
    service: str
    severity: str
    status: str
    owner: Optional[str] = None
    slack_channel: Optional[str] = None
    slack_message_ts: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    resolved_at: Optional[str] = None
