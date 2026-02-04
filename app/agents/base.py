# Esse agente será responsável por:
# - Recebe uma pergunta do usuário
# - Busca contextos relevantes no vetor store (RAG)
# - Chama o LLM com a pergunta + contexto
# - Retorna resposta estruturada

from abc import ABC, abstractmethod # Importa ABC para criar uma classe abstrata
from typing import List, Dict, Any, Optional

from app.services.llm import LLMService
from app.vectorstore.store import VectorStore 

class BaseAgent(ABC):
    """
    Classe base para todos os agentes do DocuMind AI. 

    Responsabilidades:
    - Executar fluxo RAG
    - Buscar contexto relevante
    - Chamar LLM
    - Padronizar interface dos agentes
    """

    def __init__(
        self,
        llm_service: LLMService,
        vector_store: VectorStore,
        top_k: int = 5
    ):
        self.llm_service = llm_service
        self.vector_store = vector_store
        self.top_k = top_k

    # ==========================
    # PUBLIC API
    # ==========================

    def run(self, query: str) -> str:
        """
        Executa o agente:
        - Embedding da query
        - Busca de contexto
        - Geração da resposta
        """

        query_embedding = self.llm.embed_text(query)

        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=self.top_k
        )

        context = self._build_context(results)

        prompt = self._build_prompt(
            query = query,
            context = context
        )

        return self.llm.generate(
            system_prompt=self.system_prompt(),
            prompt=prompt
        )
    
    # ==========================
    # INTERNAL METHODS
    # ==========================

    def _build_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Constrói o contexto textual a partir dos documentos recuperados.
        """

        contexts = []

        for r in results:
            text = r.get("text")
            metadata =r.get("metadata", {})

            source = metadata.get("source", "document") # Nome do documento/fonte
            page = metadata.get("page") # Número da página, se disponível

            header = f"[Fonte: {source}"
            if page is not None:
                header += f", Página: {page}" # Adiciona número da página se disponível
            header += "]"

            contexts.append(f"{header}\n{text}") # Adiciona fonte e texto

        return "\n\n".join(contexts) 
    
    # ==========================
    # ABSTRACT METHODS
    # ==========================

    @abstractmethod
    def system_prompt(self) -> str:
        """
        Prompt de sistema do agente.
        """
        raise NotImplementedError

    @abstractmethod
    def build_prompt(self, query: str, context: str) -> str:
        """
        Prompt final enviado ao LLM.
        """
        raise NotImplementedError