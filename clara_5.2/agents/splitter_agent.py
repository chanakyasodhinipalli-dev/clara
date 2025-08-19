from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from core.logger import get_logger
from core.utils import detect_mime
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class SplitterAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        mime = detect_mime(path)
        outputs: List[Dict[str, Any]] = []
        out_dir = self.ctx.outputs_dir / "split"
        out_dir.mkdir(parents=True, exist_ok=True)

        if mime == "application/pdf":
            from PyPDF2 import PdfReader, PdfWriter
            reader = PdfReader(str(path))
            for i, _ in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                out_path = out_dir / f"{path.stem}_page_{i+1}.pdf"
                with open(out_path, "wb") as f:
                    writer.write(f)
                outputs.append({"filename": out_path.name, "path": str(out_path)})
        elif mime in ("image/tiff", "image/tif"):
            from PIL import Image, ImageSequence
            im = Image.open(str(path))
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                out_path = out_dir / f"{path.stem}_page_{i+1}.tiff"
                frame.save(out_path)
                outputs.append({"filename": out_path.name, "path": str(out_path)})
        else:
            # single image or docx: copy as-is
            out_path = out_dir / path.name
            out_path.write_bytes(Path(path).read_bytes())
            outputs.append({"filename": out_path.name, "path": str(out_path)})

        return {"agent": "splitter", "input": str(path), "documents": outputs, "outputs": [o["path"] for o in outputs]}
