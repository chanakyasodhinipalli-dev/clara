from __future__ import annotations
from .base import AgentResult
from ..utils.text import redact

def run(text: str) -> AgentResult:
    data = redact(text)
    return AgentResult(True, data)
