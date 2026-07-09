from pydantic import BaseModel, Field
from typing import Optional

class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = ""
    severity: str = Field(default="medium")

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    channel_id: Optional[str] = None
    message_ts: Optional[str] = None
