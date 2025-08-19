"""
TranslationAgent
- run(text: str, src_lang: str, config: dict) -> (translated_text, confidence)
Uses simple transformers model if enabled otherwise returns original text.
"""
from core.logger import logger
from core.config_loader import load_yaml_config

try:
    from transformers import pipeline
except Exception:
    pipeline = None

class TranslationAgent:
    def __init__(self, config_path="config/app_config.yaml"):
        cfg = load_yaml_config(config_path)
        self.enabled = cfg.get("ai_flags", {}).get("translation", False)
        self.pipeline = None
        if self.enabled and pipeline:
            try:
                self.pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
            except Exception:
                self.pipeline = None

    def run(self, text, src_lang):
        if not self.enabled or not self.pipeline:
            return text, 1.0
        try:
            res = self.pipeline(text[:4000])
            return res[0]['translation_text'], 0.9
        except Exception as e:
            logger.warning("Translation failed: %s", e)
            return text, 0.0
