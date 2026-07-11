from schemas.incident import IncidentResponse


def summarize_incident(incident: IncidentResponse) -> str:
    """
    Generate a concise summary of the incident.

    This is currently a placeholder.
    Later it will call the LLM.
    """

    return (
        f"Incident '{incident.title}' is affecting the "
        f"{incident.service} service. "
        f"Current severity is '{incident.severity}'. "
        f"Investigation is in progress."
    )