# Architecture

- **FastAPI backend** (`src/clara/api`) serving UI and workflow endpoints.
- **Orchestrator** (`src/clara/orchestrator/workflow.py`) implements Sequential and Parallel fan-out patterns.
- **Agents** (`src/clara/agents/*`) each return **Structured JSON** with `success`, `data`, `metrics`.
- **AI Providers** (`src/clara/ai/*`) pluggable; disabled when `ai_enabled=false`.
- **Config**: `data/config/config.yaml` + `.env` environment override.
- **UI**: Server-rendered (Jinja2) + HTMX + Tailwind CDN. Embedded PDF viewer.
- **Workspace**: uploads and outputs under `workspace/`.

## Patterns
- ReAct used by Context and Classification Agents when AI enabled.
- Generator–Critic: Summarizer + Reviewer pass; Reflexion logs when confidence low.
- Iterative Refinement: Metadata extraction loops until threshold or max retries.
