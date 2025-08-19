from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from collections import Counter
import re
from core.logger import get_logger
from .base import AgentBase

logger = get_logger(__name__)

def simple_summarize(text: str, sentences: int = 3) -> str:
    # naive frequency-based summarizer
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sents) <= sentences:
        return text
    words = re.findall(r'\w+', text.lower())
    freq = Counter(words)
    scored = sorted(((sum(freq[w.lower()] for w in re.findall(r'\w+', s)), i, s) for i, s in enumerate(sents)), reverse=True)
    top = sorted(scored[:sentences], key=lambda x: x[1])
    return " ".join(s for _,_,s in top)

@dataclass
class SummarizationAgent(AgentBase):
    def run(self, path: Path) -> Dict[str, Any]:
        text = self._extract_text(path)
        native_summary = simple_summarize(text, sentences=int(self.cfg.get("sentences", 3)))
        english_summary = native_summary

        if self.ctx.ai.cfg.enabled:
            prompt = f"Summarize in original language and English:\n{text[:2000]}"
            ai_out = self.ctx.ai.prompt(prompt)
            if ai_out:
                english_summary = ai_out

        return {
            "agent": "summarization",
            "input": str(path),
            "summary_native": native_summary,
            "summary_english": english_summary,
            "outputs": [str(path)],
        }

    def _extract_text(self, path: Path) -> str:
        from core.utils import detect_mime
        mime = detect_mime(path)
        try:
            if mime == "application/pdf":
                from pdfminer.high_level import extract_text
                return extract_text(str(path)) or ""
            elif mime.startswith("image/"):
                import pytesseract
                from PIL import Image
                return pytesseract.image_to_string(Image.open(str(path)))
            elif mime.endswith("document"):
                from docx import Document
                doc = Document(str(path))
                return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            logger.warning(f"SummarizationAgent text extraction failed: {e}")
        return ""
