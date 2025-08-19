from __future__ import annotations
import concurrent.futures as futures
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Callable
import yaml

from .logger import get_logger
from .ai_client import AIClient, AIConfig

logger = get_logger(__name__)

@dataclass
class Context:
    app_dir: Path
    outputs_dir: Path
    temp_dir: Path
    ai: AIClient
    config: Dict[str, Any]

class Orchestrator:
    def __init__(self, app_dir: Path):
        self.app_dir = app_dir
        self.config_dir = app_dir / "config"
        self.outputs_dir = app_dir / "outputs"
        self.temp_dir = app_dir / "temp"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.config = self._load_yaml(self.config_dir / "app.yaml")
        self.workflows = self._load_yaml(self.config_dir / "workflows.yaml")
        ai_cfg = AIConfig(enabled=bool(self.config.get("ai_enabled", False)))
        self.ctx = Context(app_dir, self.outputs_dir, self.temp_dir, AIClient(ai_cfg), self.config)

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _load_agent(self, name: str):
        # dynamic import via mapping
        from importlib import import_module
        module_map = {
            "preprocessor": "agents.preprocessor_agent",
            "splitter": "agents.splitter_agent",
            "merger": "agents.merger_agent",
            "context": "agents.context_agent",
            "translation": "agents.translation_agent",
            "summarization": "agents.summarization_agent",
            "classification": "agents.classification_agent",
            "metadata": "agents.metadata_extraction_agent",
            "grouping": "agents.grouping_agent",
            "converted": "agents.converted_agent",
            "ocr": "agents.ocr_agent",
            "redaction": "agents.redaction_agent",
        }
        if name not in module_map:
            raise ValueError(f"Unknown agent: {name}")
        mod = import_module(module_map[name])
        return getattr(mod, f"{name.capitalize()}Agent")

    def run_workflow(self, workflow_name: str, inputs: List[Path]) -> Dict[str, Any]:
        wf = self.workflows.get(workflow_name)
        if not wf:
            raise ValueError(f"Workflow '{workflow_name}' not found in config/workflows.yaml")
        steps: List[Dict[str, Any]] = wf.get("steps", [])
        current_inputs = inputs
        all_results: Dict[str, Any] = {"workflow": workflow_name, "steps": []}

        for step in steps:
            agent_name = step["agent"]
            parallel = step.get("parallel", False)
            AgentCls = self._load_agent(agent_name)
            agent = AgentCls(self.ctx, step.get("config", {}))
            logger.info(f"Running step: {agent_name} (parallel={parallel}) on {len(current_inputs)} input(s)")

            if parallel and len(current_inputs) > 1:
                with futures.ThreadPoolExecutor(max_workers=min(8, len(current_inputs))) as ex:
                    futs = [ex.submit(agent.run, p) for p in current_inputs]
                    results = [f.result() for f in futs]
            else:
                results = [agent.run(p) for p in current_inputs]

            all_results["steps"].append({"agent": agent_name, "results": results})
            # Flatten outputs for next step if paths returned
            next_inputs: List[Path] = []
            for r in results:
                if r and isinstance(r, dict):
                    outs = r.get("outputs") or r.get("documents") or []
                    for d in outs:
                        if isinstance(d, dict) and "path" in d:
                            next_inputs.append(Path(d["path"]))
                        elif isinstance(d, str):
                            next_inputs.append(Path(d))
            current_inputs = next_inputs if next_inputs else current_inputs
        return all_results
