from schemas.incident import IncidentResponse


def recommend_actions(
    incident: IncidentResponse,
) -> list[str]:
    """
    Recommend next actions.
    Placeholder implementation.
    """

    return [
        "Check service health.",
        "Review recent deployments.",
        "Inspect application logs.",
        "Notify the incident owner.",
    ]