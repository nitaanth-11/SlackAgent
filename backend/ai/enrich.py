from schemas.incident import IncidentResponse
from schemas.ai_response import AIEnrichmentResponse
from ai.pipeline.pipeline import run_ai_pipeline

def enrich_incident(
    incident: IncidentResponse,
) -> AIEnrichmentResponse:
    """
    Main entry point for incident enrichment.

    For now this returns mock AI output.
    Later it will call the real LLM pipeline.
    """
    return run_ai_pipeline(incident)