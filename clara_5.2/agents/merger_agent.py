from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from core.logger import get_logger
from core.utils import detect_mime
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class MergerAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        # 'path' may be a directory or a single file. If directory, merge all PDFs there.
        inputs: List[Path] = []
        if Path(path).is_dir():
            inputs = sorted([p for p in Path(path).iterdir() if p.suffix.lower() == ".pdf"])
        else:
            inputs = [Path(path)]

        out_dir = self.ctx.outputs_dir / "merged"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"merged_{Path(path).stem}.pdf"

        from PyPDF2 import PdfWriter, PdfReader
        writer = PdfWriter()
        for p in inputs:
            if detect_mime(p) == "application/pdf":
                reader = PdfReader(str(p))
                for page in reader.pages:
                    writer.add_page(page)
        with open(out_path, "wb") as f:
            writer.write(f)

        return {"agent": "merger", "input": str(path), "filename": out_path.name, "path": str(out_path), "outputs": [str(out_path)]}
