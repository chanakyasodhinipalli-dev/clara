from __future__ import annotations
import logging
import logging.config
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..config import settings
from .routes import router as api_router
import yaml

# Logging
log_cfg = Path(__file__).resolve().parents[3] / "src" / "clara" / "logging_conf.yaml"
with log_cfg.open("r", encoding="utf-8") as f:
    logging.config.dictConfig(yaml.safe_load(f))

import logging

logging.getLogger("watchfiles").setLevel(logging.WARNING)

app = FastAPI(title="Clara 7.0")

static_dir = Path(__file__).resolve().parents[1] / "ui" / "static"
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "ui" / "templates"))

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("clara.api.main:app", host="127.0.0.1", port=8000, reload=True)
