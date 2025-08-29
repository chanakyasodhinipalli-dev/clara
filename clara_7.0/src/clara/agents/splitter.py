from __future__ import annotations
from pathlib import Path
from typing import List
from .base import AgentResult
from ..utils.pdf_utils import split_pdf

def run(path: Path) -> AgentResult:
    if path.suffix.lower() == ".pdf":
        pages: List[Path] = split_pdf(path)
        return AgentResult(True, {"pages": [str(p) for p in pages], "count": len(pages)})
    return AgentResult(True, {"pages": [str(path)], "count": 1})
