from schemas.ai_response import (
    AIEnrichmentResponse,
    SeverityPrediction,
    ProbableCause,
    RunbookReference,
    SimilarIncident,
)


def get_mock_enrichment():
    return AIEnrichmentResponse(
        summary="The Payments API is experiencing elevated latency, causing failed customer requests.",

        severity=SeverityPrediction(
            label="SEV-2",
            confidence=0.92,
            reason="Customer-facing service degradation with significant impact."
        ),

        probable_causes=[
            ProbableCause(
                cause="Database connection pool exhaustion",
                confidence=0.86
            )
        ],

        suggested_actions=[
            "Check database health.",
            "Review recent deployments.",
            "Scale API instances if required."
        ],

        related_runbooks=[
            RunbookReference(
                title="Payments API Runbook",
                section="Database Connectivity",
                score=0.95
            )
        ],

        similar_incidents=[
            SimilarIncident(
                incident_id="INC-041",
                title="Database latency spike",
                similarity=0.91
            )
        ],

        stakeholder_update_draft=(
            "We are investigating elevated latency affecting the Payments API. "
            "Engineers have identified the issue and mitigation is underway."
        ),

        postmortem_draft=None
    )