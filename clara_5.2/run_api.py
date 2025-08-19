from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from core.orchestrator import Orchestrator
from core.logger import get_logger
from api.routes import router as api_router
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = FastAPI(title="Clara 5.0")
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).resolve().parents[0] / "ui" / "static")),
    name="static"
)
app.mount("/outputs", StaticFiles(directory=str(Path(__file__).resolve().parents[1] / "outputs")), name="outputs")

env = Environment(
    loader=FileSystemLoader(str(Path(__file__).resolve().parents[0] / "templates")),
    autoescape=select_autoescape()
)

logger = get_logger(__name__)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    template = env.get_template("index.html")
    orch = Orchestrator(Path(__file__).resolve().parents[1])
    workflows = list(orch.workflows.keys())
    return template.render(workflows=workflows)

@app.get("/download/{filename}")
async def download(filename: str):
    out_path = Path(__file__).resolve().parents[1] / "outputs" / filename
    if not out_path.exists():
        return HTMLResponse(f"File not found: {filename}", status_code=404)
    return FileResponse(str(out_path))

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
