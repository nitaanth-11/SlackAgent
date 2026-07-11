from schemas.incident import IncidentResponse
from schemas.ai_response import ProbableCause


def find_probable_causes(
    incident: IncidentResponse,
) -> list[ProbableCause]:
    """
    Generate probable root causes.
    Placeholder implementation.
    """

    return [
        ProbableCause(
            cause="Possible infrastructure or database issue.",
            confidence=0.80,
        )
    ]