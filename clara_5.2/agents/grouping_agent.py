from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, DefaultDict
from dataclasses import dataclass
from collections import defaultdict
from core.logger import get_logger
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class GroupingAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        # In orchestrated mode, ContextAgent should have produced group ids.
        # Standalone: each file becomes its own group.
        group_id = f"group_{path.stem}"
        group_dir = self.ctx.outputs_dir / "groups" / group_id
        group_dir.mkdir(parents=True, exist_ok=True)
        dest = group_dir / path.name
        dest.write_bytes(Path(path).read_bytes())
        return {"agent": "grouping", "input": str(path), "group": group_id, "outputs": [str(dest)]}
