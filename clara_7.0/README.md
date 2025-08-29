# Clara 7.0

Agentic AI Workflow Orchestrator Framework for multi-lingual and multi-contextual document processing with a web UI.

## Quickstart (Windows & Linux)

```bash
# 1) Create venv
python -m venv .venv
# 2) Activate
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
# 3) Install deps
pip install -r requirements.txt
To update, run: python.exe -m pip install --upgrade pip
# 4) (Optional) configure AI
copy .env.example .env   # or cp .env.example .env
# Edit .env and set AI_ENABLED=true and provider key
# 5) Run API
pip install -e .
python -m clara.api.main
# Open UI:
# http://127.0.0.1:8000
```

## Features
- Sequential + Parallel fan-out/gather orchestration
- Generator–Critic, ReAct, Reflexion, Iterative Refinement patterns
- Config-driven AI (OpenAI or Gemini) — toggle via `data/config/config.yaml` or `.env`
- Web UI: file upload, submit, JSON view, table output, collapsible sections, embedded PDF viewer, downloadable links

See `ARCHITECTURE.md` for diagrams and details.
