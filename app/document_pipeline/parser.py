# Recebe Documentos corporativos (PDF, DOCX, TXT, etc.) e os converte em texto bruto.
# Normaliza a saída, para ser usada por(chunking, embedding, etc).
# Utilizando o Docling library

from pathlib import Path
from typing import Dict, Any
import logging

from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)

class DocumentParser:
    """
    Responsável por converter documentos corporativos (PDF, DOCX, TXT, etc.)
    em texto estruturado utilizando Docling.

    Saída normalizada para:
    - Chunking
    - Embeddings
    - Agentes de IA
    """

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path: Path) -> Dict[str, Any]:
        """
        Converte um documento em estrutura textual normalizada.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        logger.info(f"Convertendo documento: {path.name}")

        try:
            result = self.converter.convert(path)

            # O document vem dentro do result
            document = result.document

            return self._normalize_document(document, path)

        except Exception as e:
            logger.exception(f"Erro ao converter o documento {path.name}")
            raise e

    def _normalize_document(self, document, path: Path) -> Dict[str, Any]:
        """
        Normaliza a saída do Docling em um formato
        consistente e fácil de consumir por IA.
        """

        pages = []

        # A API atual do Docling expõe pages dessa forma
        for idx, page in enumerate(document.pages):
            text = page.text if hasattr(page, "text") else ""

            pages.append({
                "page_number": idx + 1,
                "text": text.strip() if text else "",
            })

        full_text = "\n".join(p["text"] for p in pages if p["text"])

        return {
            "file_name": path.name,
            "file_type": path.suffix.lower(),
            "num_pages": len(pages),
            "text": full_text,
            "pages": pages,
        }