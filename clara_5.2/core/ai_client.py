from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
from .logger import get_logger

logger = get_logger(__name__)

@dataclass
class AIConfig:
    enabled: bool = False
    provider: Optional[str] = None  # e.g., 'openai'
    model: Optional[str] = None

class AIClient:
    def __init__(self, cfg: AIConfig):
        self.cfg = cfg

    def prompt(self, prompt_text: str, meta: Optional[Dict[str, Any]] = None) -> str:
        if not self.cfg.enabled:
            logger.info("AI disabled; returning rule-based placeholder response.")
            return ""  # agents must handle fallback logic
        # Placeholder without external dependency; real integration can be added by user.
        # We just echo trimmed prompt tail to simulate a response.
        tail = prompt_text.strip()[-300:]
        logger.warning("AI enabled but no provider configured. Returning heuristic echo response.")
        return f"[AI_SIMULATED_RESPONSE]\n{tail}"
