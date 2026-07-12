from ai.llm import get_provider
from ai.pipeline.summarizer import summarize_incident
from ai.pipeline.severity import classify_severity
from ai.pipeline.root_cause import find_probable_causes
from ai.pipeline.actions import recommend_actions

from schemas.incident import IncidentResponse
from schemas.ai_response import AIEnrichmentResponse


def run_ai_pipeline(
    incident: IncidentResponse,
) -> AIEnrichmentResponse:

    provider = get_provider()

    # Temporary
    return provider.enrich(incident)