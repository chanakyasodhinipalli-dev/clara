from sentence_transformers import SentenceTransformer
import numpy as np

class ContextModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception:
            self.model = None

    def embed(self, texts):
        if self.model:
            emb = self.model.encode(texts, show_progress_bar=False)
            return [list(x) for x in emb]
        # fallback: simple TF-IDF not implemented here; return zero vectors
        return [[0.0]*384 for _ in texts]
