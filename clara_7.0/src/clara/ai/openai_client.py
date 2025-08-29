from __future__ import annotations
import os
import httpx
import logging
import base64
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")

    async def chat_json(
        self,
        system: str,
        user: str,
        schema: Dict[str, Any],
        files: Optional[List[Path]] = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            logger.error("AI disabled or missing key")
            return {"error": "AI disabled or missing key"}

        # Prepare messages
        messages = [
            {"role": "system", "content": system}
        ]
        user_content = user

        # Prepare images and text as OpenAI "content" blocks
        content_blocks = []
        if user_content:
            content_blocks.append({"type": "text", "text": user_content})

        if files:
            for file_path in files:
                suffix = file_path.suffix.lower()
                if suffix in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"]:
                    with open(file_path, "rb") as f:
                        img_bytes = f.read()
                        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                    content_blocks.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{suffix[1:] if suffix != '.jpg' else 'jpeg'};base64,{img_b64}"
                        }
                    })
                else:
                    try:
                        text_content = file_path.read_text(encoding="utf-8")
                    except Exception:
                        text_content = f"[Non-text file: {file_path.name}]"
                    content_blocks.append({"type": "text", "text": text_content})

        if content_blocks:
            messages.append({"role": "user", "content": content_blocks})

        # Add schema instruction
        schema_instruction = f"Return JSON matching this schema: {schema}"
        messages.append({"role": "user", "content": schema_instruction})

        url = f"{self.api_base}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        logger.info("Sending request to OpenAI: url=%r, payload=%r", url, payload)
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=payload, headers=headers, timeout=60)
                resp.raise_for_status()
                content = resp.json()
                logger.info("Received response from OpenAI: %r", content)
                import json as pyjson
                text = content["choices"][0]["message"]["content"]
                # Remove markdown code block if present
                import re
                text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()
                # Find the first JSON-like object
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                # Replace single quotes with double quotes for valid JSON
                json_str = json_str.replace("'", '"')
                return pyjson.loads(json_str)
            except Exception as e:
                logger.error("Error parsing OpenAI response: %r", e, exc_info=True)
                return {"error": "Could not parse AI response", "raw": resp.json() if 'resp' in locals() else None}
