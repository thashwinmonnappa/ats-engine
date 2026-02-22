import pdfplumber
import docx

class ResumeParser:

    def extract_text(self, file_path: str) -> str:
        if file_path.endswith(".pdf"):
            return self._extract_pdf(file_path)
        elif file_path.endswith(".docx"):
            return self._extract_docx(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError("Unsupported file format")

    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def _extract_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])