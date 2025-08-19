from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
from core.logger import get_logger
from core.utils import detect_mime
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class OcrAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        text = ""
        try:
            import pytesseract
            from PIL import Image
            mime = detect_mime(path)
            if mime == "application/pdf":
                # Convert first page to image if poppler is present
                from pdf2image import convert_from_path
                images = convert_from_path(str(path), dpi=200, first_page=1, last_page=1)
                if images:
                    text = pytesseract.image_to_string(images[0])
            elif mime.startswith("image/"):
                text = pytesseract.image_to_string(Image.open(str(path)))
        except Exception as e:
            logger.warning(f"OCR failed (check Tesseract/Poppler): {e}")

        return {"agent": "ocr", "input": str(path), "text": text, "outputs": [str(path)]}
