from io import BytesIO

class ContractTools:
    """
    Simple tools used by Agno agents: extract contract text from PDF/DOCX/TXT bytes.
    """
    def get_contract(self, file_bytes: bytes, filename: str) -> str:
        name = (filename or "").lower().strip()

        if name.endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(file_bytes))
            pages = []
            for p in reader.pages:
                pages.append(p.extract_text() or "")
            return "\n\n".join(pages).strip()

        if name.endswith(".docx"):
            import docx
            doc = docx.Document(BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs]).strip()

        try:
            return file_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1", errors="ignore").strip()
