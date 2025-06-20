import os
from typing import Tuple
from PyPDF2 import PdfReader
import pdfplumber
import docx
from PIL import Image
import pytesseract
import tempfile

SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.txt']


def extract_text_from_pdf(file_path: str) -> str:
    # Try text extraction with PyPDF2
    try:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
        if text.strip():
            return text
    except Exception:
        pass
    # Fallback to pdfplumber
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or '' for page in pdf.pages)
            if text.strip():
                return text
    except Exception:
        pass
    # Fallback to OCR
    return ocr_pdf(file_path)


def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def ocr_pdf(file_path: str) -> str:
    # Convert each page to image and run OCR
    import fitz  # PyMuPDF
    try:
        import fitz
    except ImportError:
        return "[OCR not available: install PyMuPDF]"
    text = ""
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
            pix.save(tmp_img.name)
            img = Image.open(tmp_img.name)
            text += pytesseract.image_to_string(img) + "\n"
            os.unlink(tmp_img.name)
    return text


def extract_text(file_path: str) -> Tuple[str, str]:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path), 'pdf'
    elif ext == '.docx':
        return extract_text_from_docx(file_path), 'docx'
    elif ext == '.txt':
        return extract_text_from_txt(file_path), 'txt'
    else:
        raise ValueError(f"Unsupported file type: {ext}") 