from __future__ import annotations
import json
from pathlib import Path
from .base import AgentResult
from ..config import settings
from ..ai.openai_client import OpenAIClient
from ..ai.gemini_client import GeminiClient

async def run(text: str) -> AgentResult:
    prompts = Path(__file__).resolve().parents[3] / "data" / "config" / "prompts" / "summarize.json"
    conf = json.loads(prompts.read_text(encoding="utf-8"))
    if settings.ai_enabled:
        client = OpenAIClient() if settings.ai_provider == "openai" else GeminiClient()
        resp = await client.chat_json(conf["system"], text, conf["schema"])
        return AgentResult(True, resp)
    # Fallback deterministic summary
    return AgentResult(True, {"summary": text[:500], "language": "en", "confidence": 0.5})
