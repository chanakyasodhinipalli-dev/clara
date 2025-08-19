from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from core.logger import get_logger
from core.utils import detect_mime
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class ContextAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        # Rule mode: group by filename patterns (front/back, page numbers), else each page new group
        mime = detect_mime(path)
        group_id = None
        label = "document"
        name = Path(path).stem.lower()

        if "aadhaar" in name and ("front" in name or "back" in name):
            group_id = f"aadhaar_{name.replace('front','').replace('back','').strip('_-')}"
            label = "aadhaar"
        elif "pan" in name:
            group_id = "pan_card"
            label = "pan"
        elif any(k in name for k in ["bank", "statement"]):
            group_id = "bank_statement"
            label = "bank_statement"
        elif "address" in name:
            group_id = "address_proof"
            label = "address_proof"
        else:
            group_id = f"group_{abs(hash(name)) % 10_000}"

        if self.ctx.ai.cfg.enabled:
            prompt = f"""Group this page with either previous context or new:
File: {path.name}
Heuristics: aadhaar front/back, pan, address proof, bank statement, continuation.
"""
            _ = self.ctx.ai.prompt(prompt)

        return {
            "agent": "context",
            "input": str(path),
            "group": {"id": group_id, "label": label, "continuation": label in {"bank_statement"}},
            "outputs": [str(path)],
        }
