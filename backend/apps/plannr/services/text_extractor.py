import os
from pathlib import Path
import pypdf
import docx

def extract_text_from_file(file_path):
    """
    Extracts text from a file (PDF, DOCX, or TXT).
    Args:
        file_path (str or Path): Path to the file.
    Returns:
        str: Extracted text.
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if not path.exists():
        return ""
        
    try:
        if ext == '.pdf':
            return _extract_from_pdf(path)
        elif ext == '.docx':
            return _extract_from_docx(path)
        elif ext == '.txt':
            return path.read_text(encoding='utf-8', errors='ignore')
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def _extract_from_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def _extract_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])
