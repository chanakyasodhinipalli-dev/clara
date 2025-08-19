"""
ClassificationAgent
- __init__(rules: list[dict]) or pass rules_path in .from_rules_path
- run(text: str) -> dict with docTypeCode, docTypeDescription, assumed, regulatoryRiskFlags, classification_confidence
"""
from typing import List, Dict
from core.logger import logger

class ClassificationAgent:
    def __init__(self, rules: List[Dict]):
        # rules should be list of dicts from load_doc_rules
        self.rules = rules

    @classmethod
    def from_rules_path(cls, path):
        from core.config_loader import load_doc_rules
        rules = load_doc_rules(path)
        return cls(rules)

    def run(self, text: str) -> Dict:
        t = text.lower()
        best = None
        best_score = -1
        for r in self.rules:
            reqs = r.get("requiredKeywords", [])
            opts = r.get("optionalKeywords", [])
            required_match = True
            if reqs:
                required_match = all(req in t for req in reqs)
            optional_matches = sum(1 for opt in opts if opt in t)
            score = optional_matches + (10 if required_match else 0)
            if score > best_score:
                best_score = score
                best = (r, required_match, optional_matches)
        if not best or best_score <= 0:
            return {
                "docTypeCode": "UNKNOWN",
                "docTypeDescription": "Unclassified",
                "assumed": True,
                "regulatoryRiskFlags": [],
                "classification_confidence": 0.0
            }
        r, required_match, optional_matches = best
        # normalize confidence (simple)
        conf = min(1.0, (optional_matches / max(1, len(r.get("optionalKeywords",[]))) ) * 0.7 + (0.3 if required_match else 0.0))
        return {
            "docTypeCode": r["docTypeCode"],
            "docTypeDescription": r["docTypeDescription"],
            "assumed": r.get("assumed", False),
            "regulatoryRiskFlags": r.get("regulatoryRiskFlags", []),
            "classification_confidence": round(conf, 2)
        }
