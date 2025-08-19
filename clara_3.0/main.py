import argparse
from api.controller import run_pipeline
import json, os

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="Path to file")
parser.add_argument("--folder", help="Path to folder")
args = parser.parse_args()

if args.file:
    out = run_pipeline(args.file)
    print(json.dumps(out, indent=2, ensure_ascii=False))
elif args.folder:
    results = []
    for f in os.listdir(args.folder):
        path = os.path.join(args.folder, f)
        if os.path.isfile(path):
            try:
                results.append({f: run_pipeline(path)})
            except Exception as e:
                results.append({f: str(e)})
    print(json.dumps(results, indent=2, ensure_ascii=False))
else:
    parser.print_help()
