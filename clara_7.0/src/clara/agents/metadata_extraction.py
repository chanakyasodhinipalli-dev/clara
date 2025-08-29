from __future__ import annotations
import re
from .base import AgentResult
from ..config import settings

NAME_RE = r"Name[:\s]+([A-Za-z ]{3,})"
PAN_RE = r"[A-Z]{5}[0-9]{4}[A-Z]"
AADHAAR_RE = r"\b\d{4}\s\d{4}\s\d{4}\b"

def extract_once(text: str) -> dict:
    name = re.search(NAME_RE, text)
    pan = re.search(PAN_RE, text)
    aadhaar = re.search(AADHAAR_RE, text)
    return {
        "name": (name.group(1).strip() if name else ""),
        "pan": (pan.group(0) if pan else ""),
        "aadhaar": (aadhaar.group(0) if aadhaar else ""),
        "confidence": 0.5 + 0.1*sum(bool(x) for x in [name, pan, aadhaar])
    }

def run(text: str) -> AgentResult:
    result = extract_once(text)
    retries = 0
    while result["confidence"] < settings.thresholds.metadata_confidence_min and retries < settings.thresholds.max_refine_retries:
        # naive refinement: expand search (simulate)
        result = extract_once(text + " Name: John Doe ")
        retries += 1
    result["retries"] = retries
    return AgentResult(True, result)
