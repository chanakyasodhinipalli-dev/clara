from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Paths:
    uploads_dir: Path
    outputs_dir: Path

@dataclass
class Thresholds:
    metadata_confidence_min: float
    max_refine_retries: int

@dataclass
class AIConfig:
    openai: dict
    gemini: dict  # This will now include 'model'

@dataclass
class Settings:
    ai_enabled: bool
    ai_provider: str
    log_level: str
    ai: AIConfig
    paths: Paths
    thresholds: Thresholds

def _env_expand(val: str) -> str:
    # Simple ${VAR:default} expansion
    if isinstance(val, str) and val.startswith("${") and val.endswith("}"):
        body = val[2:-1]
        if ":" in body:
            var, default = body.split(":", 1)
            return os.getenv(var, default)
        return os.getenv(body, "")
    return val

def _expand_mapping(m):
    if isinstance(m, dict):
        return {k: _expand_mapping(_env_expand(v)) for k, v in m.items()}
    return _env_expand(m)

def load_settings() -> Settings:
    cfg_path = Path(__file__).resolve().parents[2] / "data" / "config" / "config.yaml"
    with cfg_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    raw = _expand_mapping(raw)

    uploads = Path(raw["paths"]["uploads_dir"]); uploads.mkdir(parents=True, exist_ok=True)
    outputs = Path(raw["paths"]["outputs_dir"]); outputs.mkdir(parents=True, exist_ok=True)
    return Settings(
        ai_enabled=str(raw["ai_enabled"]).lower() == "true",
        ai_provider=str(raw["ai_provider"]).lower(),
        log_level=str(raw["log_level"]).upper(),
        ai=AIConfig(
            openai=raw.get("ai", {}).get("openai", {}),
            gemini=raw.get("ai", {}).get("gemini", {}),
        ),
        paths=Paths(uploads_dir=uploads, outputs_dir=outputs),
        thresholds=Thresholds(
            metadata_confidence_min=float(raw["thresholds"]["metadata_confidence_min"]),
            max_refine_retries=int(raw["thresholds"]["max_refine_retries"]),
        ),
    )

settings = load_settings()
