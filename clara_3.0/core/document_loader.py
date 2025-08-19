import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from core.logger import logger
from core.config_loader import load_yaml_config

def extract_text_from_pdf(path: str, poppler_path: str = None):
    texts = []
    try:
        # Try direct text extraction via PyMuPDF
        doc = fitz.open(path)
        for page in doc:
            txt = page.get_text().strip()
            texts.append(txt if txt else "")
        doc.close()
        # If pages have empty text, fallback to pdf2image->OCR for those pages
        if any(not t for t in texts):
            raise ValueError("Some pages empty, fallback to image OCR")
        return texts
    except Exception as e:
        logger.info("Falling back to image-based extraction: %s", e)
        # image-based conversion + OCR
        pil_pages = convert_from_path(path, poppler_path=poppler_path) if poppler_path else convert_from_path(path)
        texts = []
        for img in pil_pages:
            text = pytesseract.image_to_string(img)
            texts.append(text.strip())
        return texts

def extract_text_from_image(image_path: str):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img).strip()
