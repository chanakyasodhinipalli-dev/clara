from __future__ import annotations
import csv
from pathlib import Path
from .base import AgentResult
from ..config import settings

def run(text: str) -> AgentResult:
    cfg = Path(__file__).resolve().parents[3] / "data" / "config" / "classification_config.csv"
    label = "UNKNOWN"
    with cfg.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["pattern"].lower() in text.lower():
                label = row["label"]; break
    return AgentResult(True, {"label": label, "confidence": 0.6 if label!='UNKNOWN' else 0.3, "mode": "config"})
