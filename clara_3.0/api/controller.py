import os
import json
import zipfile
from datetime import datetime
from core.config_loader import load_yaml_config, load_doc_rules
from core.logger import logger
from agents.splitter_agent import SplitterAgent
from agents.context_agent import ContextAgent
from agents.grouping_agent import GroupingAgent
from agents.language_agent import LanguageAgent
from agents.translation_agent import TranslationAgent
from agents.summarization_agent import SummarizationAgent
from agents.classification_agent import ClassificationAgent
from agents.risk_detection_agent import RiskDetectionAgent
from agents.metadata_agent import MetadataAgent
from agents.summary_agent import SummaryAgent
from core.prompt_manager import PromptManager
import fitz  # PyMuPDF

CONFIG = load_yaml_config("config/app_config.yaml")
PROMPTS = PromptManager(CONFIG.get("paths", {}).get("prompts", "config/prompts.yaml"))

def _make_output_folder():
    out = CONFIG.get("paths", {}).get("output_folder", "./output")
    os.makedirs(out, exist_ok=True)
    return out

def run_pipeline(file_path: str):
    logger.info("Pipeline starting for %s", file_path)
    out_folder = _make_output_folder()
    # 1. Splitter
    splitter = SplitterAgent()
    pages = splitter.run(file_path)
    if not pages:
        raise RuntimeError("No pages extracted")

    # 2. Context / embeddings
    contexter = ContextAgent()
    pages = contexter.run(pages)

    # 3. Grouping
    grouper = GroupingAgent()
    groups = grouper.run(pages)

    # load classification rules once
    rules = load_doc_rules(CONFIG.get("paths", {}).get("doc_rules"))
    classifier = ClassificationAgent(rules)
    risk_detector = RiskDetectionAgent(rules)
    meta_agent = MetadataAgent()
    lang_agent = LanguageAgent()
    trans_agent = TranslationAgent()
    summarizer = SummarizationAgent()
    summarizer_agent = SummaryAgent()

    groups_out = []
    for idx, group in enumerate(groups, start=1):
        text = " ".join([p["text"] if isinstance(p, dict) else str(p) for p in group]).strip()
        pages_range = [p.get("page_number") if isinstance(p, dict) else i+1 for i,p in enumerate(group)]
        # language
        lang_info = lang_agent.run(text)
        is_trans = CONFIG.get("ai_flags", {}).get("translation", False) and lang_info.get("language") != "en"
        translated_text, trans_conf = trans_agent.run(text, lang_info.get("language"))
        # summarize
        sum_orig, sum_orig_conf = summarizer.run(text)
        sum_trans, sum_trans_conf = (None, None)
        if is_trans:
            sum_trans, sum_trans_conf = summarizer.run(translated_text)
        # classify
        class_res = classifier.run(text)
        doc_code = class_res.get("docTypeCode")
        doc_desc = class_res.get("docTypeDescription")
        assumed = class_res.get("assumed")
        class_conf = class_res.get("classification_confidence", 0.0)
        # risk
        risks, risk_conf = risk_detector.run(text)
        # metadata
        metadata = meta_agent.run(text)
        # reasoning
        reasoning = summarizer_agent.reason(text, class_res)

        group_obj = {
            "groupId": f"group_{idx}",
            "pageRange": pages_range,
            "language": lang_info.get("language"),
            "isTranslationRequired": is_trans,
            "translatedText": translated_text if is_trans else None,
            "originalText": text,
            "summaryOriginalLanguage": sum_orig,
            "summaryTranslatedEnglish": sum_trans,
            "docTypeCode": doc_code,
            "docTypeDescription": doc_desc,
            "assumed": assumed,
            "regulatoryRiskFlags": risks,
            "metadataSummary": metadata,
            "confidenceScores": {
                "languageDetection": round(lang_info.get("confidence", 0.0), 2),
                "translation": round(trans_conf or 0.0, 2),
                "summarization": round(sum_orig_conf or 0.0, 2),
                "classification": round(class_conf or 0.0, 2),
                "riskDetection": round(risk_conf or 0.0, 2)
            },
            "aiReasoning": reasoning
        }
        groups_out.append(group_obj)

    result = {
        "detectedMimeType": "application/pdf",
        "isValidMimeType": True,
        "routingDecision": "Proceed to OCR" if CONFIG.get("file_handling",{}).get("allowed_extensions") else "Unknown",
        "mimeConfidence": 0.99,
        "groups": groups_out
    }

    # export metadata JSON and group PDFs and zip
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(file_path))[0]
    meta_name = f"{base}_metadata_{timestamp}.json"
    meta_path = os.path.join(out_folder, meta_name)
    with open(meta_path, "w", encoding="utf-8") as mf:
        json.dump(result, mf, indent=2, ensure_ascii=False)
    zip_name = f"{base}_groups_{timestamp}.zip"
    zip_path = os.path.join(out_folder, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(meta_path, arcname=os.path.basename(meta_path))
        # write group PDFs using PyMuPDF: extract pages into new PDF per group
        src = fitz.open(file_path)
        for gidx, group in enumerate(groups, start=1):
            gp_pdf = os.path.join(out_folder, f"{base}_group_{gidx}.pdf")
            new_doc = fitz.open()
            for p in group:
                pno = p.get("page_number", None)
                if pno is None:
                    continue
                new_doc.insert_pdf(src, from_page=pno-1, to_page=pno-1)
            new_doc.save(gp_pdf)
            new_doc.close()
            zf.write(gp_pdf, arcname=os.path.basename(gp_pdf))
        src.close()

    result["downloadZip"] = f"/download/{os.path.basename(zip_path)}"
    logger.info("Pipeline completed for %s", file_path)
    return result
