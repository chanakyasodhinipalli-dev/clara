from __future__ import annotations
import os
import httpx
import re
import logging
import base64
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: str = None, api_base: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_base = api_base or os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta")
        self.model = model or os.getenv("GEMINI_MODEL", "models/gemini-1.5-flash-latest")

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

        prompt = (
            f"{system}\n"
            f"User input:\n{user}\n"
            f"Return JSON matching this schema: {schema}"
        )

        # Prepare parts: always start with the prompt as text
        parts = [{"text": prompt}]

        # Add files as parts
        if files:
            for file_path in files:
                suffix = file_path.suffix.lower()
                if suffix in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"]:
                    # Image file: encode as base64
                    with open(file_path, "rb") as f:
                        img_bytes = f.read()
                        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                    parts.append({
                        "inline_data": {
                            "mime_type": f"image/{suffix[1:] if suffix != '.jpg' else 'jpeg'}",
                            "data": img_b64
                        }
                    })
                else:
                    # Text file: read and add as text
                    try:
                        text_content = file_path.read_text(encoding="utf-8")
                    except Exception:
                        text_content = f"[Non-text file: {file_path.name}]"
                    parts.append({"text": text_content})

        url = f"{self.api_base}/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {"role": "user", "parts": parts}
            ]
        }
        logger.info("Sending request to Gemini AI: url=%r, payload=%r", url, payload)
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                content = resp.json()
                logger.info("Received response from Gemini AI: %r", content)
                import json as pyjson
                text = content["candidates"][0]["content"]["parts"][0]["text"]
                # Remove markdown code block if present
                text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()
                # Find the first JSON-like object
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                # Replace single quotes with double quotes for valid JSON
                json_str = json_str.replace("'", '"')
                return pyjson.loads(json_str)
            except Exception as e:
                logger.error("Error parsing Gemini AI response: %r", e, exc_info=True)
                return {"error": "Could not parse AI response", "raw": resp.json() if 'resp' in locals() else None}
