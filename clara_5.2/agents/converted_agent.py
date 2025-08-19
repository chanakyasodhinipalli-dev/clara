from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
from core.logger import get_logger
from core.utils import detect_mime
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class ConvertedAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        mime = detect_mime(path)
        out_dir = self.ctx.outputs_dir / "converted"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{path.stem}.pdf"

        try:
            if mime.startswith("image/"):
                from PIL import Image
                im = Image.open(str(path)).convert("RGB")
                im.save(out_path, "PDF", resolution=100.0)
            elif mime == "application/pdf":
                out_path.write_bytes(Path(path).read_bytes())
            elif mime.endswith("document"):
                # Simple docx to PDF workaround: dump text to a PDF-like image-based PDF
                from docx import Document
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import A4
                doc = Document(str(path))
                text = "\n".join(p.text for p in doc.paragraphs)
                c = canvas.Canvas(str(out_path), pagesize=A4)
                width, height = A4
                y = height - 50
                for line in text.splitlines():
                    c.drawString(40, y, line[:120])
                    y -= 14
                    if y < 40:
                        c.showPage()
                        y = height - 50
                c.save()
            else:
                out_path.write_bytes(Path(path).read_bytes())
        except Exception as e:
            logger.warning(f"ConvertedAgent failed, copying as-is: {e}")
            out_path.write_bytes(Path(path).read_bytes())

        return {"agent": "converted", "input": str(path), "filename": out_path.name, "path": str(out_path), "outputs": [str(out_path)]}
