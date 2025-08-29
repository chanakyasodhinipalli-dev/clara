from __future__ import annotations
from pathlib import Path
from typing import List
from .base import AgentResult
from ..utils.pdf_utils import merge_pdfs

def run(pages: List[Path], groups: list[list[int]], out_path: Path) -> AgentResult:
    # For simplicity, merge all pages when single group; else merge per group then final
    if not groups:
        merged = merge_pdfs(pages, out_path)
        return AgentResult(True, {"merged": str(merged)})
    out_files = []
    for gi, group in enumerate(groups):
        part = out_path.parent / f"{out_path.stem}_part{gi+1}.pdf"
        subset = [pages[i] for i in group]
        merge_pdfs(subset, part)
        out_files.append(str(part))
    final = merge_pdfs([Path(p) for p in out_files], out_path)
    return AgentResult(True, {"merged": str(final), "parts": out_files})
