"""
SummarizationAgent
- run(text: str) -> (summary, confidence)
Uses a transformer summarizer if enabled, otherwise extractive stub.
"""
from core.logger import logger
from core.config_loader import load_yaml_config
try:
    from transformers import pipeline
except Exception:
    pipeline = None

class SummarizationAgent:
    def __init__(self, config_path="config/app_config.yaml"):
        cfg = load_yaml_config(config_path)
        self.enabled = cfg.get("ai_flags", {}).get("summarization", False)
        self.pipeline = None
        if self.enabled and pipeline:
            try:
                self.pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            except Exception:
                self.pipeline = None

    def run(self, text: str):
        if not text:
            return "", 0.0
        if not self.enabled or not self.pipeline:
            # simple extractive: first 2 sentences or first 200 chars
            s = " ".join(text.split(".")[:2]).strip()
            return (s[:400] + "...") if s else (text[:200] + "..."), 0.8
        try:
            out = self.pipeline(text[:4000], max_length=150, min_length=30)
            return out[0]['summary_text'], 0.9
        except Exception as e:
            logger.warning("Summarization failed: %s", e)
            s = " ".join(text.split(".")[:2]).strip()
            return (s[:400] + "...") if s else (text[:200] + "..."), 0.6
