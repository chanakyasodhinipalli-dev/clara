from __future__ import annotations
from pathlib import Path
from .base import AgentResult

def run(path: Path) -> AgentResult:
    mime = "application/pdf" if path.suffix.lower()==".pdf" else "image" if path.suffix.lower() in {".png",".jpg",".jpeg",".tif",".tiff"} else "text/plain"
    return AgentResult(True, {"mime": mime, "name": path.name})
