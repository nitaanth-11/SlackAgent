from abc import ABC, abstractmethod

from schemas.incident import IncidentResponse
from schemas.ai_response import AIEnrichmentResponse


class BaseAIProvider(ABC):
    @abstractmethod
    def enrich(
        self,
        incident: IncidentResponse,
    ) -> AIEnrichmentResponse:
        """
        Return AI enrichment for an incident.
        """
        pass