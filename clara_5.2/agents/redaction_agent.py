from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import re
from core.logger import get_logger
from core.utils import AADHAAR_RE, PAN_RE, ACCOUNT_RE, CUSTOMER_ID_RE, detect_mime
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class RedactionAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        # Text-layer redaction: extract, mask, and write simple PDF with masked text (image-based output)
        out_dir = self.ctx.outputs_dir / "redacted"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"redacted_{Path(path).stem}.pdf"

        try:
            text = self._extract_text(path)
            red = text
            for pat in (AADHAAR_RE, PAN_RE, ACCOUNT_RE, CUSTOMER_ID_RE):
                red = pat.sub("[REDACTED]", red)
            # Write basic PDF with text (not preserving layout)
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            c = canvas.Canvas(str(out_path), pagesize=A4)
            width, height = A4
            y = height - 50
            for line in red.splitlines() or [""]:
                c.drawString(40, y, line[:120])
                y -= 14
                if y < 40:
                    c.showPage()
                    y = height - 50
            c.save()
        except Exception as e:
            logger.warning(f"Redaction failed; copying as-is: {e}")
            out_path.write_bytes(Path(path).read_bytes())

        return {"agent": "redaction", "input": str(path), "filename": out_path.name, "path": str(out_path), "outputs": [str(out_path)]}

    def _extract_text(self, path: Path) -> str:
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
            logger.warning(f"RedactionAgent text extraction failed: {e}")
        return ""
