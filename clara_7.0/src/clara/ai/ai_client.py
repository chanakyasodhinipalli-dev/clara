from ..config import settings
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient

def get_ai_client():
    if settings.ai_provider == "openai":
        return OpenAIClient(
            api_key=settings.ai.openai.get("api_key"),
            api_base=settings.ai.openai.get("api_base"),
            model=settings.ai.openai.get("model"),
        )
    else:
        return GeminiClient(
            api_key=settings.ai.gemini.get("api_key"),
            api_base=settings.ai.gemini.get("api_base"),
            model=settings.ai.gemini.get("model"),
        )