from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.routes import router as api_router
import uvicorn
import os

app = FastAPI(title="Clara UI")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="ui/static"), name="static")
templates = Jinja2Templates(directory="ui/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    uvicorn.run("ui.web_app:app", host="0.0.0.0", port=8000, reload=True)
