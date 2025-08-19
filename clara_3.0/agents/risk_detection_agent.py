"""
RiskDetectionAgent
- __init__(rules: list[dict]) or pass rules_path
- run(text: str) -> (flags: list[str], confidence: float)
"""
from typing import List
from core.logger import logger

class RiskDetectionAgent:
    def __init__(self, rules=None):
        # rules not strictly needed, we use keywords present in rules to flag
        self.rules = rules or []

    def run(self, text: str):
        t = text.lower()
        flags = set()
        for r in self.rules:
            for kw in (r.get("requiredKeywords",[]) + r.get("optionalKeywords",[])):
                if kw and kw in t:
                    for f in r.get("regulatoryRiskFlags", []):
                        if f:
                            flags.add(f)
        return list(flags), (0.9 if flags else 0.0)
