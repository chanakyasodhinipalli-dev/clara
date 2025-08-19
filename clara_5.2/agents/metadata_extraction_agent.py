from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import re
from core.logger import get_logger
from core.utils import AADHAAR_RE, PAN_RE, ACCOUNT_RE, CUSTOMER_ID_RE
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class MetadataAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        text = self._extract_text(path)
        meta = {
            "name": self._guess_name(text),
            "customer_id": self._first(CUSTOMER_ID_RE.findall(text)),
            "aadhaar": self._first(AADHAAR_RE.findall(text)),
            "pan": self._first(PAN_RE.findall(text)),
            "account_number": self._first(ACCOUNT_RE.findall(text)),
            "address": self._guess_address(text),
        }
        if self.ctx.ai.cfg.enabled:
            prompt = f"Extract entities (name, customer id, aadhaar, pan, account, address):\n{text[:2000]}"
            _ = self.ctx.ai.prompt(prompt)
        return {"agent": "metadata", "input": str(path), "metadata": meta, "outputs": [str(path)]}

    def _extract_text(self, path: Path) -> str:
        from core.utils import detect_mime
        mime = detect_mime(path)
        try:
            if mime == "application/pdf":
                from pdfminer.high_level import extract_text
                return extract_text(str(path)) or ""
            elif mime.startswith("image/"):
                import pytesseract
                from PIL import Image
                return pytesseract.image_to_string(Image.open(str(path)))
            elif mime.endswith("document"):
                from docx import Document
                doc = Document(str(path))
                return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            logger.warning(f"MetadataAgent text extraction failed: {e}")
        return ""

    def _guess_name(self, text: str) -> str:
        m = re.search(r'Name[:\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
        return m.group(1) if m else ""

    def _guess_address(self, text: str) -> str:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for i, l in enumerate(lines):
            if "address" in l.lower() and i + 1 < len(lines):
                return lines[i+1][:200]
        return ""

    def _first(self, seq):
        return seq[0] if seq else ""
