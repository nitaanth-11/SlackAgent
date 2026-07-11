from ollama import Client

from ai.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)
from ai.mock.mock_ai import get_mock_enrichment
from ai.prompts.summarizer import (
    SYSTEM_PROMPT,
    build_summary_prompt,
)
from ai.providers.base import BaseAIProvider
from schemas.incident import IncidentResponse
from schemas.ai_response import AIEnrichmentResponse


class OllamaProvider(BaseAIProvider):

    def __init__(self):
        self.client = Client(host=OLLAMA_BASE_URL)

    def enrich(
        self,
        incident: IncidentResponse,
    ) -> AIEnrichmentResponse:

        prompt = build_summary_prompt(
            incident.title,
            incident.description,
            incident.service,
        )

        # Actual Ollama call will come next.
        # Keeping mock response until JSON parsing is ready.

        response = self.client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        print(response)

        return get_mock_enrichment()