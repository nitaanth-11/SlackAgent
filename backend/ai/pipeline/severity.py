from schemas.incident import IncidentResponse
from schemas.ai_response import SeverityPrediction


def classify_severity(incident: IncidentResponse) -> SeverityPrediction:
    """
    Classify incident severity.
    Placeholder implementation.
    """

    return SeverityPrediction(
        label=incident.severity.upper(),
        confidence=0.90,
        reason="Initial severity based on incident metadata."
    )