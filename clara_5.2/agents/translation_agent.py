from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
from core.logger import get_logger
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class TranslationAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        # Rule mode: identity translation (no external connectivity). Logs that it's a noop.
        # AI mode: simulated via AIClient echo.
        text = self._extract_text(path)
        translated = text

        if self.ctx.ai.cfg.enabled:
            prompt = f"Translate to English while keeping key entities: {text[:1500]}"
            ai_out = self.ctx.ai.prompt(prompt)
            if ai_out:
                translated = ai_out

        return {"agent": "translation", "input": str(path), "translated_text": translated, "outputs": [str(path)]}

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
            logger.warning(f"TranslationAgent text extraction failed: {e}")
        return ""
