from __future__ import annotations
from pathlib import Path
from .base import AgentResult
try:
    import pytesseract
    from PIL import Image
except Exception:  # Pillow/pytesseract may be missing
    pytesseract = None
    Image = None

def run(path: Path) -> AgentResult:
    if pytesseract and Image and path.suffix.lower() in {".png",".jpg",".jpeg",".tif",".tiff"}:
        text = pytesseract.image_to_string(Image.open(path))
        return AgentResult(True, {"text": text})
    return AgentResult(True, {"text": ""}, message="OCR skipped (not image or dependency missing)")
