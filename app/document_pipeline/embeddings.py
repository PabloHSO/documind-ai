# O Embeddings é reponsável por:
# - Trasnformar chunks em vetores numéricos
# - Ser agnóstico de provedor (HuggingFace, OpenAI, etc.)

from typing import List, Dict
import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)
 
class EmbeddingsGenerator:
    """
    Responsável por gerar embeddings vetoriais
    a partir de chunks de texto.

    Implementação inicial usando HuggingFace
    (Sentence Transformers).
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Args:
            model_name (str): Modelo HuggingFace para embeddings
        """
        logger.info(f"Carregando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name) # Carrega o modelo de embeddings

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:

        """
        Gera embeddings para uma lista de chunks.

        Args:
            chunks (List[Dict]): Lista de chunks estruturados

        Returns:
            List[Dict]: Chunks com embeddings adicionados
        """
         
        texts = [chunk["text"] for chunk in chunks]
    
        if not texts:

            return []
    
        logger.info(f"Gerando embeddings para {len(texts)} chunks")
    
        vectors = self.model.encode(
            texts, 
            show_progress_bar=False,
            normalize_embeddings=True
        ) # Gera os embeddings
    
        enriched_chunks = []
    
        for chunk, vector in zip(chunks, vectors):
            enriched_chunks.append({
                **chunk, 
                "embedding": vector.tolist()
                })
        
        return enriched_chunks
    
