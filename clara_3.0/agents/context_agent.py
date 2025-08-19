"""
ContextAgent
- run(pages: List[dict]) -> pages with added 'embedding' list
"""
from core.context_model import ContextModel
from core.logger import logger
from core.config_loader import load_yaml_config
import numpy as np

class ContextAgent:
    def __init__(self, config_path="config/app_config.yaml"):
        cfg = load_yaml_config(config_path)
        model_name = cfg.get("grouping", {}).get("embedding_model", "all-MiniLM-L6-v2")
        self.model = ContextModel(model_name)

    def run(self, pages):
        texts = [p.get("text","") for p in pages]
        embeddings = self.model.embed(texts)
        for p, emb in zip(pages, embeddings):
            p["embedding"] = emb
        return pages
