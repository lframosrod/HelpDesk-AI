import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extrae todo el texto de un PDF directamente desde sus bytes en memoria."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            full_text.append(f"--- Página {page_num} ---\n{text}")
    doc.close()
    return "\n\n".join(full_text)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Divide el texto largo en fragmentos superpuestos para preservar el contexto semántico."""
    if not text:
        return []
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks