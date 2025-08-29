from __future__ import annotations
from typing import Any, Dict, Protocol

class AIClient(Protocol):
    async def chat_json(self, system: str, user: str, schema: Dict[str, Any]) -> Dict[str, Any]: ...
