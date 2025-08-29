from __future__ import annotations
from pathlib import Path
from .base import AgentResult

def run(path: Path) -> AgentResult:
    # Deterministic step: return same file for demo
    return AgentResult(True, {"converted": str(path)})
