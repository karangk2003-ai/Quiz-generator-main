import os
import fitz  # PyMuPDF
from docx import Document

class DocumentService:
    @staticmethod
    def extract_text(file_path):
        """Extract text from the given file based on its extension."""
        ext = file_path.rsplit('.', 1)[1].lower()
        
        try:
            if ext == 'txt':
                return DocumentService._extract_from_txt(file_path)
            elif ext == 'pdf':
                return DocumentService._extract_from_pdf(file_path)
            elif ext == 'docx':
                return DocumentService._extract_from_docx(file_path)
            else:
                raise ValueError("Unsupported file format.")
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")

    @staticmethod
    def _extract_from_txt(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def _extract_from_pdf(file_path):
        text = ""
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            # Fallback or just re-raise
            raise e
        return text

    @staticmethod
    def _extract_from_docx(file_path):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
