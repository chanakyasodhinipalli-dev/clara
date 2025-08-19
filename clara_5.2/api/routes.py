from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from core.orchestrator import Orchestrator
from core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/process-folder")
async def process_folder(folder: str = Form(...), workflow: str = Form(...)):
    app_dir = Path(__file__).resolve().parents[1]
    orch = Orchestrator(app_dir)
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        raise HTTPException(400, detail="Folder not found")
    inputs = [x for x in p.iterdir() if x.is_file()]
    result = orch.run_workflow(workflow, inputs)
    return JSONResponse(result)

@router.post("/upload")
async def upload(file: UploadFile = File(...), workflow: str = Form(...)):
    app_dir = Path(__file__).resolve().parents[1]
    tmp_dir = app_dir / "temp" / "uploads"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    dest = tmp_dir / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    orch = Orchestrator(app_dir)
    result = orch.run_workflow(workflow, [dest])
    return JSONResponse(result)
