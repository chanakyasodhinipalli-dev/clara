from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import asyncio
from ..config import settings
from ..utils.io import derive_output_path
from ..utils.pdf_utils import split_pdf
from ..agents import preprocessor, splitter, ocr, context, translation, summarization, reviewer, classification, metadata_extraction, grouping, merger, redaction, converter
from ..agents.base import AgentResult

async def _gather_parallel(texts: list[str]) -> Dict[str, Any]:
    # Fan-out: translation, summarization, classification run in parallel per whole text
    # For demo, join texts
    joined = "\n\n".join(texts)
    summ_task = asyncio.create_task(summarization.run(joined))
    clsf_task = asyncio.create_task(asyncio.to_thread(lambda: classification.run(joined)))
    trans_task = asyncio.create_task(asyncio.to_thread(lambda: translation.run(joined)))
    results = await asyncio.gather(summ_task, clsf_task, trans_task)
    sum_r, cls_r, tr_r = results
    rev = reviewer.run(sum_r.data.get("summary",""))
    return {
        "translation": tr_r.dict(),
        "summary": sum_r.dict(),
        "review": rev.dict(),
        "classification": cls_r.dict(),
    }

async def run_full(path: Path) -> Dict[str, Any]:
    pre = preprocessor.run(path)
    split = splitter.run(path)
    page_paths = [Path(p) for p in split.data["pages"]]

    # OCR/text extraction for downstream steps
    texts = []
    for p in page_paths:
        r = ocr.run(p)
        texts.append(r.data.get("text", ""))

    # Run context agent per page in parallel
    from ..agents.context import run_single
    context_tasks = []
    prev_content = None
    for i, p in enumerate(page_paths):
        context_tasks.append(run_single(p, prev_content))
        prev_content = texts[i]  # Use OCR text as previous content

    context_results = await asyncio.gather(*context_tasks)
    continuations = [r.data.get("continuation", False) for r in context_results]
    structural_analyses = [r.data.get("structural_analysis", "") for r in context_results]
    page_contexts = [r.data.get("page_context", "") for r in context_results]
    ctx = AgentResult(True, {
        "continuations": continuations,
        "structural_analyses": structural_analyses,
        "page_contexts": page_contexts
    })

    grp = grouping.run(ctx.data["continuations"])

    # Merge into single PDF
    out_pdf = derive_output_path(path, settings.paths.outputs_dir, "_merged.pdf")
    mrg = merger.run(page_paths, grp.data["groups"], out_pdf)

    # Redaction + Metadata on joined text
    joined = "\n\n".join(texts) if texts else ""
    red = redaction.run(joined)
    meta = metadata_extraction.run(joined)

    # Parallel AI-ish tasks
    parallel = await _gather_parallel(texts)

    # Converter deterministic
    conv = converter.run(path)

    return {
        "preprocessor": pre.dict(),
        "splitter": split.dict(),
        "context": ctx.dict(),
        "grouping": grp.dict(),
        "merger": mrg.dict(),
        "redaction": red.dict(),
        "metadata": meta.dict(),
        "parallel": parallel,
        "converter": conv.dict(),
        "outputs": {
            "merged_pdf": mrg.data.get("merged"),
        }
    }
