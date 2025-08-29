from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from ..config import settings
from ..utils.io import save_upload
from ..orchestrator.workflow import run_full

router = APIRouter()

@router.post("/api/process")
async def process_file(file: UploadFile = File(...)):
    try:
        path = save_upload(file, settings.paths.uploads_dir)
        result = await run_full(path)
        return JSONResponse({"ok": True, "input_file": str(path), "result": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/file")
def get_file(path: str):
    p = Path(path).resolve()
    if not p.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(p), filename=p.name)
