from __future__ import annotations
import re
import mimetypes
from pathlib import Path
from typing import Tuple, List

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff'}
PDF_EXTS = {'.pdf'}
DOCX_EXTS = {'.docx'}

def detect_mime(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return f'image/{ext.lstrip(".")}'
    if ext in PDF_EXTS:
        return 'application/pdf'
    if ext in DOCX_EXTS:
        return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    # fallback
    return mimetypes.guess_type(str(path))[0] or 'application/octet-stream'

AADHAAR_RE = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')
PAN_RE = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b')
ACCOUNT_RE = re.compile(r'\b\d{9,18}\b')
CUSTOMER_ID_RE = re.compile(r'\bCID[- ]?\d{4,10}\b', re.I)

def chunk_text(text: str, size: int = 2000) -> List[str]:
    return [text[i:i+size] for i in range(0, len(text), size)]

def safe_filename(name: str) -> str:
    return re.sub(r'[^\w\-\.]+', '_', name).strip('_')
