# O store é reponsável por:
# - Armazenar embeddings em memória (MVP)
# - Fazer busca semântica por similaridade
# - Ser simples, rápido e 100% gratuito
# - Facilmente trocável depois por FAISS, Chroma, Pinecone etc.

from typing import List, Dict
import numpy as np
import logging

logger = logging.getLogger(__name__)

class InMemoryVectorStore:
    """
    Vetor store simples em memória para MVP.

    Responsabilidades:
    - Armazenar embeddings
    - Executar busca por similaridade (cosine)
    """

    def __init__(self):
        self.vectors: List[np.ndarray] = [] # Lista de embeddings
        self.documents: List[Dict] = [] # Metadados dos documentos

    def add_documents(self, docs: List[Dict]):
        """
        Adiciona documentos vetorizados ao store.

        Args:
            docs (List[Dict]): Lista de chunks com embeddings
        """

        for doc in docs:
            embedding = np.array(doc["embedding"], dtype=np.float32)
            self.vectors.append(embedding)
            self.documents.append(doc)

        logger.info(f"Adicionados {len(docs)} documentos ao vetor store.")

    def similarity_search(
            self,
            query_embedding: List[float],
            top_k: int = 5
        ) -> List[Dict]: 
            """
            Retorna os top_k documentos mais similares.

            Args:
                query_embedding (List[float]): Vetor da query
                top_k (int): Quantidade de resultados

            Returns:
                List[Dict]: Documentos mais similares
            """

            if not self.vectors:
                return []
            
            query_vec = np.array(query_embedding, dtype=np.float32) # Converte a query em numpy array

            similarities = [
                 self._cosine_similarity(query_vec, vec)
                    for vec in self.vectors
            ] # Calcula similaridades

            top_indices = np.argsort(similarities)[-top_k:][::-1] # Índices dos top_k mais similares (argsort - ordena)

            results = []
            for idx in top_indices:
                doc = self.documents[idx].copy()
                doc["score"] = similarities[idx]
                results.append(doc)
            
            return results
    
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        Calcula similaridade cosseno entre dois vetores.
        """
        denom = np.linalg.norm(a) * np.linalg.norm(b) # Normalização (linalg - norma do vetor)
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom) # Produto escalar dividido pela normalização
    