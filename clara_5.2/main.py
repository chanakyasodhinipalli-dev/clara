from __future__ import annotations
import argparse
from pathlib import Path
from core.orchestrator import Orchestrator
from core.logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Clara 5.0 CLI")
    parser.add_argument("--workflow", required=True, help="Workflow name from config/workflows.yaml")
    parser.add_argument("--input", required=True, help="File or folder path")
    args = parser.parse_args()

    app_dir = Path(__file__).resolve().parent
    orch = Orchestrator(app_dir)
    p = Path(args.input)
    inputs = []
    if p.is_dir():
        inputs = [x for x in p.iterdir() if x.is_file()]
    else:
        inputs = [p]
    result = orch.run_workflow(args.workflow, inputs)
    print(result)

if __name__ == "__main__":
    main()
