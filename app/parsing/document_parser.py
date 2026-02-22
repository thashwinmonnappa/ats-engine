import pdfplumber
import docx
import os

class DocumentParser:

    def extract_text(self, input_source: str) -> str:
        """
        Accepts:
        - file path (.pdf, .docx, .txt)
        - or raw text string
        """

        if os.path.exists(input_source):
            if input_source.endswith(".pdf"):
                return self._extract_pdf(input_source)
            elif input_source.endswith(".docx"):
                return self._extract_docx(input_source)
            elif input_source.endswith(".txt"):
                return self._extract_txt(input_source)
            else:
                raise ValueError("Unsupported file format")
        else:
            # Assume raw text
            return input_source

    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def _extract_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()