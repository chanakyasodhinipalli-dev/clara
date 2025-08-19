# Clara 5.0 — Agentic AI Workflow Orchestrator (Python)

**Version:** 5.0 • **Python:** 3.11+ • **OS:** Windows & Linux

Clara 5.0 is an **Agentic AI Workflow Orchestrator** for **multi‑lingual, multi‑contextual document processing**.  
It ships with a FastAPI UI, robust logging, fully-typed code, rule‑based fallbacks, and optional AI paths gated by config.

> ⚠️ External binaries required for some features:
> - **Tesseract OCR** (for OCR): install and add to PATH
> - **Poppler** (for PDF → image via `pdf2image` on Windows): install and add `bin` to PATH

---

## Quick Start

```bash
# 1) Create venv (Windows)
python -m venv .venv
.venv\Scripts\activate

# 1) Create venv (Linux/Mac)
python -m venv .venv
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run API + UI
python run_api.py  # serves http://127.0.0.1:8000

# 4) CLI processing (examples)
python main.py --workflow full_pipeline --input samples/demo_docs
python main.py --workflow splitter_only --input samples/demo_docs
```

### Windows notes
- Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/ and add `poppler-xx\Library\bin` to PATH.

### Linux notes
- `sudo apt-get install tesseract-ocr poppler-utils`

---

## Features (Rule-first, AI-optional)

- Agents can run **standalone** or orchestrated.
- **AI used only when `config/app.yaml` sets `ai_enabled: true`**. Otherwise, deterministic logic.
- Multi-format input: **PDF, PNG, JPG, JPEG, TIFF**, DOCX.
- **Parallel** execution supported where appropriate.
- **Workflows** configured in `config/workflows.yaml`.

---

## Project Layout
```
clara_5.0
├── agents/                  # Document agents
├── api/                     # FastAPI endpoints + templates
├── core/                    # Core libs: logger, orchestrator, utils
├── config/                  # App/workflow/prompt configs
├── ui/                      # Static + HTML templates
├── tests/                   # Unit tests (pytest)
├── outputs/                 # Generated at runtime
├── samples/                 # Sample JSON and demo docs
├── temp/                    # Runtime temp
├── requirements.txt
├── main.py                  # CLI entry
├── run_api.py               # FastAPI server
└── README.md
```

---

## Config Overview

- `config/app.yaml` — global app flags (ai_enabled, ocr_enabled, paths).
- `config/workflows.yaml` — declares orchestrated steps. Example workflows provided.
- `config/classification.csv` — type config for ClassificationAgent (code, name, desc, rule).
- `config/prompts/*.txt` — prompts used when AI is enabled (no network calls unless you integrate your own client).

---

## UI

`http://127.0.0.1:8000`

- Drag‑drop upload, choose workflow, process.
- PDF preview, collapsible JSON, download buttons per `group_{id}.pdf` and ZIP.

---

## API

- `POST /api/process-folder` → body: `{ "folder": "...", "workflow": "..." }`
- `POST /api/upload` → multipart upload with `file` + `workflow`
- `GET /download/{filename}` → serves from `outputs/`

---

## Testing

```bash
pytest -q
```

- AI is mocked. Tests use tiny sample files and synthetic content.

---

## Offline & Fallbacks

- If AI or external binaries are missing, Clara logs a **warning** and falls back to deterministic logic.
- OCR/PDF conversion gracefully degrade if Tesseract/Poppler are not found.

---

## License

MIT
