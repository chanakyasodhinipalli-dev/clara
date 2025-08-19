from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from api.controller import run_pipeline
import os
import uuid

router = APIRouter()

@router.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    tmp_name = f"temp_{uuid.uuid4().hex}_{file.filename}"
    tmp_path = os.path.join("temp", tmp_name)
    os.makedirs("temp", exist_ok=True)
    with open(tmp_path, "wb") as f:
        f.write(await file.read())
    try:
        result = run_pipeline(tmp_path)
        return result
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

@router.post("/api/process-folder")
async def process_folder(payload: dict):
    folder = payload.get("folder_path")
    if not folder or not os.path.isdir(folder):
        raise HTTPException(status_code=400, detail="Invalid folder_path")
    results = []
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            try:
                res = run_pipeline(fpath)
                results.append({"file": fname, "result": res})
            except Exception as e:
                results.append({"file": fname, "error": str(e)})
    return {"results": results}

@router.get("/download/{filename}")
def download(filename: str):
    path = os.path.join("output", filename)
    if os.path.exists(path):
        return FileResponse(path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")
