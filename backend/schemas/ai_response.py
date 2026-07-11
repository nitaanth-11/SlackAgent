from pydantic import BaseModel
from typing import List


class SeverityPrediction(BaseModel):
    label: str
    confidence: float
    reason: str


class ProbableCause(BaseModel):
    cause: str
    confidence: float


class RunbookReference(BaseModel):
    title: str
    section: str
    score: float


class SimilarIncident(BaseModel):
    incident_id: str
    title: str
    similarity: float


class AIEnrichmentResponse(BaseModel):
    summary: str

    severity: SeverityPrediction

    probable_causes: List[ProbableCause]

    suggested_actions: List[str]

    related_runbooks: List[RunbookReference]

    similar_incidents: List[SimilarIncident]

    stakeholder_update_draft: str

    postmortem_draft: str | None = None