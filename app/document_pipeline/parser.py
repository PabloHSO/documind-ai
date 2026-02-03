# Recebe Documentos corporativos (PDF, DOCX, TXT, etc.) e os converte em texto bruto.
# Normaliza a saída, para ser usada por(chunking, embedding, etc).
# Utilizando o Docling library

from pathlib import Path
from typing import Dict, Any
import logging

from docling.document_converter import DocumentConverter
from docling.datamodel.document import Document

logger = logging.getLogger(__name__)

class DocumentParser:
    """
    Resposável por convereter documentos corporativvos (PDF, DOCX, TXT, etc.)
    em textos estruturados utilizando Docling

    Este módulo faz parte da document_pipeline e prepara
    os dados para:
    - Chunking
    - Embeddings 
    - Agentes de IA
    """

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path: Path) -> Dict[str, Any]:
        """
        Converte um documento em estrutura textual normalizada.

        Args:
            file_path (str): Caminho do arquivo

        Returns:
            Dict[str, Any]: Documento estruturado
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        logger.info(f"Convertendo documento: {path.name}")

        try:
            result = self.converter.convert(path) # Converte o documento
            document: Document = result.document # Extrai o documento convertido

            return self._normalize_document(document, path)
        
        except Exception as e:
            logger.error(f"Erro ao converter o documento {path.name}: {e}")
            raise e
        
    def _normalize_document(self, document: Document, path: Path) -> Dict[str, Any]:
        """
        Normaliza a saída do Docling em um formato
        consistente e fácil de consumir por IA.
        """

        pages = []

        for page in document.pages:
            pages.append({
                "page_number": page.page_no,
                "text": page.text.strip() if page.text else "",
            })

        full_text = "\n".join(p["text"] for p in pages if p["text"])

        return {
            "file_name": path.name,
            "file_type": path.suffix.lower(),
            "num_pages": len(pages),
            "text": full_text,
            "pages": pages,
        }