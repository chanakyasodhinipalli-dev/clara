from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any
from core.logger import get_logger

logger = get_logger(__name__)

@dataclass
class AgentBase:
    ctx: Any
    cfg: Dict[str, Any]

    def run(self, path: Path) -> Dict[str, Any]:  # pragma: no cover
        raise NotImplementedError
