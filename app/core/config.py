from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    """
    Configurações globais do DocuMind AI.
    Todas variáveis sensíveis devem vir do .env
    """

    # ====== Application settings =======
    APP_NAME: str = "DocuMind AI"
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")

    # ====== CORS =======
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # ====== OpenAI =======
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    # ====== HuggingFace =======
    HUGGINGFACE_API_KEY: str | None = None
    HF_EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ====== Vector Store =======
    VECTOR_DB_PATH: str = Field(default="./data/vectorstore")

    # ====== Document Processing ======
    CHUNK_SIZE: int = Field(default=800)
    CHUNK_OVERLAP: int = Field(default=100)

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cacheia as configurações para evitar múltiplas leituras do .env
    """
    return Settings()
