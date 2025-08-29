from __future__ import annotations
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile
import shutil
import uuid

def save_upload(upload: UploadFile, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.filename).suffix or ""
    out = dest_dir / f"{uuid.uuid4().hex}{suffix}"
    with out.open("wb") as f:
        shutil.copyfileobj(upload.file, f)
    return out

def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def safe_stem(path: Path) -> str:
    return Path(path).stem.replace(" ", "_").replace("/", "_")

def derive_output_path(input_path: Path, outputs_dir: Path, suffix: str) -> Path:
    return outputs_dir / f"{safe_stem(input_path)}{suffix}"
