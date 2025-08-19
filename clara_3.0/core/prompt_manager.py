from typing import Dict
from jinja2 import Template
from core.config_loader import load_prompts

class PromptManager:
    def __init__(self, prompts_path: str = "config/prompts.yaml"):
        self.prompts = load_prompts(prompts_path)

    def render(self, key: str, **context) -> str:
        tpl = self.prompts.get(key, {}).get("user_prompt_template")
        if not tpl:
            return ""
        return Template(tpl).render(**context)
