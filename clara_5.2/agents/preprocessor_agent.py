from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from langdetect import detect_langs
from core.utils import detect_mime
from core.logger import get_logger
from .base import AgentBase

logger = get_logger(__name__)

@dataclass
class PreprocessorAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        mime = detect_mime(path)
        langs: List[Dict[str, Any]] = []
        multi_context = False
        text_sample = ""

        # Attempt minimal text extraction for language hints
        try:
            if mime == "application/pdf":
                from pdfminer.high_level import extract_text
                text_sample = (extract_text(str(path)) or "")[:2000]
            elif mime.startswith("image/"):
                text_sample = ""
            elif mime.endswith("document"):
                from docx import Document
                doc = Document(str(path))
                text_sample = " ".join([p.text for p in doc.paragraphs])[:2000]
        except Exception as e:
            logger.warning(f"Preprocessor text extraction failed: {e}")

        if text_sample.strip():
            try:
                det = detect_langs(text_sample)
                for d in det:
                    langs.append({"code": d.lang, "confidence": float(d.prob)})
                multi_context = len(text_sample.split("\n\n")) > 3
            except Exception as e:
                logger.warning(f"Language detection failed: {e}")

        if self.ctx.ai.cfg.enabled and not langs:
            prompt = f"""Detect languages and multi-context for the text:
{text_sample[:1000]}
"""
            ai_out = self.ctx.ai.prompt(prompt)
            if ai_out:
                langs = [{"code": "ai", "confidence": 0.5}]

        return {
            "agent": "preprocessor",
            "input": str(path),
            "mime": mime,
            "languages": langs,
            "multi_context": multi_context,
            "outputs": [str(path)],
        }
