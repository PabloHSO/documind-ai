# Preparação do arquivo para:
# - Autenticação Futura
# - Observabilidade
# - Escalabilidade
# - Testes

from fastapi import Depends
from app.services.llm import LLMService
from app.vectorstore.store import VectorStore

# =========================
# LLM Dependency
# =========================

def llm_client():
    """
    Dependency que fornece o cliente LLM.
    Facilita testes e troca futura de provider.
    """

    return LLMService()

# =========================
# Vector Store Dependency
# =========================

def vector_store():
    """
    Dependency que fornece o Vector Store.
    Mantém desacoplamento entre API e armazenamento.
    """
    return VectorStore()