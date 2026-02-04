# Fará a abstração clara de LLMs usados na aplicação
# Suporte inicial a OpenAI
# Separação entre: geração de embeddings e geração de texto
# Preparação para os agentes
# Fácil de troca para HuggingFace, etc.

from typing import List, Optional
import os
import logging
from urllib import response
from openai import OpenAI

logger = logging.getLogger(__name__)

# Fará a abstração clara de LLMs usados na aplicação
# Suporte inicial a OpenAI
# Separação entre: geração de embeddings e geração de texto
# Preparação para os agentes
# Fácil de troca para HuggingFace, etc.

from typing import List, Optional
import logging
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from app.core.config import get_settings


logger = logging.getLogger(__name__)

class LLMService:
    """
    Camada de abstração para modelos de linguagem. 

    Responsabilidades:
    - Gerar embeddings
    - Gerar respostas de texto
    - Isolar dependência de providers (OpenAI, HF, etc)
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            embedding_model: str = "text-embedding-3-small",
            chat_model: str = "gpt-4o-mini"
        ):
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY não está definido.")
            
            self.client = OpenAI(api_key=self.api_key) # Inicializa o cliente OpenAI
            self.embedding_model = embedding_model
            self.chat_model = chat_model

            logger.info("LLMService inicializado com OpenAI.")

    # ==========================
    # EMBEDDINGS
    # ==========================

    def embed_text(self, text: str) -> List[float]:
        """
        Gera embedding para um único texto.
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )

        return response.data[0].embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Gera embeddings para múltiplos textos.
        """

        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )

        return [item.embedding for item in response.data]
    
    # ==========================
    # TEXT GENERATION
    # ==========================

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> str:
        """
        Gera texto a partir de um prompt.
        """

        menssages = []

        if system_prompt:
            menssages.append({
                "role": "system",
                "content": system_prompt
            })

        menssages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model = self.chat_model,
            messages = menssages,
            temperature = temperature,
            max_tokens = max_tokens
        )

        return response.choices[0].message.content.strip()

         