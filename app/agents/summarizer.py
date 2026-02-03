# Esse agente será responsável por:
# - Receber um documento (via RAG, não tudo de uma vez)
# - Buscar trechos mais relevantes
# - Gerar: Resumo executivo, linguagem clara, foco em decisão e negócios

from app.agents.base import BaseAgent

class SummarizerAgent(BaseAgent):
    """
    Agente especializado em gerar resumos executivos
    a partir de documentos corporativos e técnicos.
    """

    def system_prompt(self) -> str:
        return (
            "Você é um analista sênior especializado em resumir documentos "
            "corporativos e técnicos para executivos, gestores e líderes. "
            "Seu objetivo é extrair os pontos mais relevantes, "
            "evitando detalhes irrelevantes e linguagem excessivamente técnica."
        )
    
    def build_prompt(self, query: str, context: str) -> str:
        """
        Constrói o prompt final para resumo.
        """
        return f"""
Abaixo estão trechos de um ou mais documentos.

CONTEXTO:
{context}

TAREFA:
Crie um resumo claro, objetivo e profissional do conteúdo acima.

INSTRUÇÕES:
- Destaque os principais temas e conclusões
- Use linguagem executiva
- Seja conciso, mas informativo
- Caso existam dados importantes, mencione-os 
- Não invente informações que não estejam no contexto

FORMATO DE SAÍDA:
Resumo executivo em parágrafos curtos.
"""
