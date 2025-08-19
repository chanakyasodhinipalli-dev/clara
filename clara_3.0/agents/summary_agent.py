"""
SummaryAgent (explainability)
- reason(text, classification_result) -> str
Uses prompt manager to create a reasoning explanation; fallback to rule-based text.
"""
from core.prompt_manager import PromptManager
from core.logger import logger

class SummaryAgent:
    def __init__(self):
        self.pm = PromptManager()

    def reason(self, text: str, classification_result: dict):
        try:
            docCode = classification_result.get("docTypeCode", "UNKNOWN")
            docDesc = classification_result.get("docTypeDescription", "")
            prompt = self.pm.render("classification_reasoning", text=text, docTypeCode=docCode, docTypeDescription=docDesc)
            if prompt and len(prompt.strip()) > 10:
                return prompt
        except Exception as e:
            logger.warning("Reasoning prompt failed: %s", e)
        # fallback
        return f"Matched {docCode} by keywords {', '.join(classification_result.get('requiredKeywords',[])[:3]) if classification_result else ''}"
