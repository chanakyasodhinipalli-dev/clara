from __future__ import annotations
from .base import AgentResult

def run(flags: list[bool]) -> AgentResult:
    # Group pages into documents; pages flagged True are continuations
    groups = []
    current = []
    for i, cont in enumerate(flags):
        if cont and current:
            current.append(i)
        else:
            if current:
                groups.append(current)
            current = [i]
    if current:
        groups.append(current)
    return AgentResult(True, {"groups": groups})
