"""
LanguageAgent
- run(text: str) -> dict {'language': 'en', 'confidence': 0.99}
"""
from langdetect import detect_langs
from core.logger import logger

class LanguageAgent:
    def run(self, text: str):
        if not text or not text.strip():
            return {"language": "unknown", "confidence": 0.0}
        try:
            langs = detect_langs(text)
            top = langs[0]
            return {"language": top.lang, "confidence": float(top.prob)}
        except Exception as e:
            logger.warning("Language detection failed: %s", e)
            return {"language": "unknown", "confidence": 0.0}
