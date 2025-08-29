from __future__ import annotations
import re
from typing import Dict

PAN_REGEX = r"[A-Z]{5}[0-9]{4}[A-Z]"
AADHAAR_REGEX = r"\b\d{4}\s\d{4}\s\d{4}\b"

def redact(text: str) -> Dict[str, str]:
    pan_found = re.findall(PAN_REGEX, text)
    aadhaar_found = re.findall(AADHAAR_REGEX, text)
    redacted = re.sub(PAN_REGEX, "[PAN_REDACTED]", text)
    redacted = re.sub(AADHAAR_REGEX, "[AADHAAR_REDACTED]", redacted)
    return {
        "text": redacted,
        "pan_matches": ", ".join(pan_found),
        "aadhaar_matches": ", ".join(aadhaar_found),
    }
