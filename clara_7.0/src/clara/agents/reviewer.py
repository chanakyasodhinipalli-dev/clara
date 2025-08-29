from __future__ import annotations
from .base import AgentResult

def run(summary: str) -> AgentResult:
    # Critic ensures summary not empty
    ok = bool(summary.strip())
    return AgentResult(ok, {"approved": ok, "notes": "" if ok else "Empty summary"})
