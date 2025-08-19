import os
import csv
import yaml
from typing import List, Dict

def load_yaml_config(path: str) -> Dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_prompts(path: str) -> Dict:
    return load_yaml_config(path)

def load_doc_rules(path: str) -> List[Dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Doc rules not found: {path}")
    rules = []
    # CSV headers as in config/doc_rules.csv
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # normalize fields
            req = [k.strip().lower() for k in row.get("requiredKeywords","").split(",") if k.strip()]
            opt = [k.strip().lower() for k in row.get("optionalKeywords","").split(",") if k.strip()]
            flags = [f.strip() for f in row.get("regulatoryRiskFlags","").split(",") if f.strip()]
            rules.append({
                "docTypeCode": row.get("docTypeCode"),
                "docTypeDescription": row.get("docTypeDescription"),
                "requiredKeywords": req,
                "optionalKeywords": opt,
                "assumed": str(row.get("assumed","false")).strip().lower() == "true",
                "regulatoryRiskFlags": flags
            })
    return rules
