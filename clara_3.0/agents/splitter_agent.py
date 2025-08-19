"""
SplitterAgent
- run(file_path: str, poppler_path: Optional[str]) -> List[dict]
Each page dict: {'page_number': int, 'text': str}
"""
from core.document_loader import extract_text_from_pdf
from core.logger import logger
from core.config_loader import load_yaml_config

class SplitterAgent:
    def __init__(self, config_path="config/app_config.yaml"):
        cfg = load_yaml_config(config_path)
        self.poppler_path = cfg.get("paths", {}).get("poppler_path") or None

    def run(self, file_path: str):
        logger.info("SplitterAgent: splitting %s", file_path)
        texts = extract_text_from_pdf(file_path, self.poppler_path)
        pages = []
        for i, t in enumerate(texts, start=1):
            pages.append({"page_number": i, "text": t})
        return pages
