from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from typing import List

def split_pdf(path: Path) -> List[Path]:
    reader = PdfReader(str(path))
    out_paths = []
    for i, _ in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        outp = path.parent / f"{path.stem}_page_{i+1}.pdf"
        with outp.open("wb") as f:
            writer.write(f)
        out_paths.append(outp)
    return out_paths

def merge_pdfs(paths: List[Path], out_path: Path) -> Path:
    writer = PdfWriter()
    for p in paths:
        reader = PdfReader(str(p))
        for pg in reader.pages:
            writer.add_page(pg)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        writer.write(f)
    return out_path
