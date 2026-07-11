from ai.mock.mock_ai import get_mock_enrichment
from ai.providers.base import BaseAIProvider
from schemas.incident import IncidentResponse
from schemas.ai_response import AIEnrichmentResponse


class OpenAIProvider(BaseAIProvider):
    def enrich(
        self,
        incident: IncidentResponse,
    ) -> AIEnrichmentResponse:

        return get_mock_enrichment()