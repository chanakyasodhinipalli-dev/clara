"""
GroupingAgent
- run(pages: List[dict], threshold: float) -> List[List[dict]]
Greedy grouping by cosine similarity to each page.
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from core.config_loader import load_yaml_config
from core.logger import logger

class GroupingAgent:
    def __init__(self, config_path="config/app_config.yaml"):
        cfg = load_yaml_config(config_path)
        self.threshold = cfg.get("grouping", {}).get("threshold", 0.82)

    def run(self, pages):
        logger.info("GroupingAgent: grouping %d pages", len(pages))
        if not pages:
            return []
        embs = [np.array(p.get("embedding") or []) for p in pages]
        n = len(embs)
        assigned = [False]*n
        groups = []
        for i in range(n):
            if assigned[i]:
                continue
            group = [pages[i]]
            assigned[i] = True
            for j in range(i+1, n):
                if assigned[j]:
                    continue
                a = embs[i].reshape(1, -1)
                b = embs[j].reshape(1, -1)
                # handle zero vectors
                try:
                    sim = float(cosine_similarity(a, b)[0][0])
                except Exception:
                    sim = 0.0
                if sim >= self.threshold:
                    group.append(pages[j])
                    assigned[j] = True
            groups.append(group)
        return groups
