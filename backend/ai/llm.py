from ai.config import LLM_PROVIDER
from ai.providers.ollama_provider import OllamaProvider
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.groq_provider import GroqProvider
from ai.providers.anthropic_provider import AnthropicProvider


def get_provider():
    if LLM_PROVIDER == "ollama":
        return OllamaProvider()

    if LLM_PROVIDER == "openai":
        return OpenAIProvider()

    if LLM_PROVIDER == "groq":
        return GroqProvider()

    if LLM_PROVIDER == "anthropic":
        return AnthropicProvider()

    raise ValueError(f"Unknown provider: {LLM_PROVIDER}")