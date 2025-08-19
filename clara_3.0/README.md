# clara_3.0 — Enterprise Document Intelligence (archive-ready)

Overview
--------
Enterprise-grade agentic document processor: page-splitting, context grouping (context-only), classification via CSV rules,
language detection, optional translation & summarization, risk detection, metadata extraction, ZIP export of group PDFs + JSON metadata.

Prereqs
-------
System:
- Python 3.11+
- Poppler (for pdf2image)
  - Windows: https://github.com/oschwartz10612/poppler-windows/releases
  - Linux: use apt/yum (e.g., `sudo apt install poppler-utils`)
- Tesseract-OCR
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - Linux: `sudo apt install tesseract-ocr`
- Add Poppler `.../poppler/bin` and Tesseract install dir to PATH or set env vars POPPLER_PATH and TESSERACT_CMD

Python
------
1. Create venv:
   python -m venv .venv
   .venv\Scripts\activate (Windows) OR source .venv/bin/activate (Linux)

2. Install packages:
   pip install -r requirements.txt

Files & Entrypoints
-------------------
- CLI: `python main.py --file path/to.pdf` or `--folder path/to/folder`
- API + UI: `python run_api.py` — UI available at http://localhost:8000

Config
------
- `config/app_config.yaml`: runtime flags & paths
- `config/prompts.yaml`: prompt templates (LLM-enabled if enabled)
- `config/doc_rules.csv`: classification rulebook

Notes
-----
- The system uses LLM/transformers only when enabled by `app_config.yaml` (`ai_flags`).
- Heavy model usage can be disabled in config to use simple rule-based fallbacks.
- Unit tests: `pytest tests/`

Support
-------
If anything fails, check logs under output/logs/app.log, ensure Poppler and Tesseract are installed and paths set.

