from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class AgentResult:
    success: bool
    data: Dict[str, Any]
    metrics: Dict[str, Any] | None = None
    message: str | None = None

    def dict(self) -> Dict[str, Any]:
        return asdict(self)
