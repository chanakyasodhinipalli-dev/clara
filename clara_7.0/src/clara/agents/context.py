from __future__ import annotations
import json
import logging
from pathlib import Path
from .base import AgentResult
from ..config import settings
from ..ai.ai_client import get_ai_client

logger = logging.getLogger(__name__)

def _read_page_content(page_path: Path) -> str:
    try:
        return page_path.read_text(encoding="utf-8")
    except Exception:
        return f"[Non-text file: {page_path.name}]"

async def run_single(page_path: Path, prev_content: str | None = None) -> AgentResult:
    logger.info("Entered run_single() with page_path=%r, prev_content=%r", page_path, prev_content)
    prompts_path = Path(__file__).resolve().parents[3] / "data" / "config" / "prompts" / "context.json"
    conf = json.loads(prompts_path.read_text(encoding="utf-8"))
    system_prompt = conf["system"]
    user_prompt_template = conf.get("user", "Current page content:\n{current_page}\n\nPrevious page content:\n{previous_page}")
    schema = conf.get("schema", {})

    current_content = _read_page_content(page_path)
    user_prompt = user_prompt_template.format(
        current_page=current_content,
        previous_page=prev_content or ""
    )

    if not settings.ai_enabled:
        # Heuristic fallback
        structural_analysis = "Simple text page" if current_content.strip() else "Blank or non-text page"
        page_context = "First page" if not prev_content else "Subsequent page"
        is_continuation = False if not prev_content else current_content.strip().lower().startswith("continued")
        result = AgentResult(True, {
            "structural_analysis": structural_analysis,
            "page_context": page_context,
            "continuation": is_continuation
        })
        logger.info("Exiting run_single() with result: %r", result)
        return result

    client = get_ai_client()
    logger.info("Invoking chat_json with system_prompt, user_prompt, schema, files")
    resp = await client.chat_json(system_prompt, user_prompt, schema, files=[page_path])
    logger.info("AI response: %r", resp)
    result = AgentResult(True, resp)
    logger.info("Exiting run_single() with result: %r", result)
    return result
