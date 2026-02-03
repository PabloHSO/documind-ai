# O Chunker é reponsável por:
# - Quebra documentos grandes em blocos inteligentes
# - Preservar contexto com overlap
# - Evitar cortar frases ao meio
# - Preparar texto para embeddings, RAG, agentes de IA

from typing import List, Dict
import logging
import re

logger = logging.getLogger(__name__)   

class TextChunker:
    """
    Responsável por dividir documentos longos em chunks
    semanticamente coerentes, com controle de tamanho e overlap.

    Ideal para:
    - Embeddings
    - RAG
    - Agentes de IA (QA, resumo, insights)
    """
 
    def __init__(
        self, 
        chunk_size: int = 800, 
        chunk_overlap: int = 150
    ):
        """
        Args:
            chunk_size (int): Tamanho máximo do chunk (em caracteres)
            chunk_overlap (int): Overlap entre chunks para manter contexto
        """
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap deve ser menor que chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split(self, text: str) -> List[str]:
        """
         Divide o texto em chunks estruturados.

        Returns:
            List[Dict]: Lista de chunks com metadados
        """
        if not text or not text.strip():
            return []
        
        sentences = self._split_sentences(text)
        chunks = []

        current_chunk = ""
        chunk_id = 0

        for sentence in sentences:
            # Se adicionar a frase ultrapassar o tamanho do chunk, salva o chunk atual
            if len(current_chunk) + len(sentence) > self.chunk_size:
                chunks.append(self.builds_chunk(current_chunk, chunk_id))
                chunk_id += 1

                # Overlap: mantém parte final do chunk anterior
                current_chunk = current_chunk[-self.chunk_overlap:]

            current_chunk += sentence + " "
        
        # Ultimo chunk
        if current_chunk.strip():
            chunks.append(self.builds_chunk(current_chunk, chunk_id))

        logger.info(f"Documento dividido em {len(chunks)} chunks.")

        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Divide o texto por sentenças para evitar cortes abruptos.
        """

        # Regex simples e eficiente para português / inglês
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _builds_chunk(self, text: str, chunk_id: int) -> str:
        """
        Estrutura padrão do chunk.
        """
        return {
            "chunk_id": chunk_id,
            "text": text.strip(),
            "length": len(text.strip())
        }


