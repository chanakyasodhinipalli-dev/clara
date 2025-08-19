from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
import pandas as pd
from core.logger import get_logger
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class ClassificationAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        csv_path = self.ctx.app_dir / "config" / "classification.csv"
        df = pd.read_csv(csv_path)
        name = path.stem.lower()
        matched = None
        for _, row in df.iterrows():
            rule = str(row.get("rule", "")).lower()
            if rule and any(tok.strip() in name for tok in rule.split("|")):
                matched = dict(row)
                break
        if not matched and self.ctx.ai.cfg.enabled:
            prompt = f"Classify document by filename and content. Filename: {path.name}"
            ai_out = self.ctx.ai.prompt(prompt)
            if ai_out:
                matched = dict(df.iloc[0])
        return {"agent": "classification", "input": str(path), "classification": matched, "outputs": [str(path)]}
