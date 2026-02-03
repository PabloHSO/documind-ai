# Esse agente será responsável por:
# - Receber uma pergunta do usuário
# - Buscar contexto relevante no VectorStore
# - Responder: (com base exclusiva nos documentos | sem alucinação | citando implicitamente o conteúdo analisado)
# Ser útil tanto para: documentos técnicos quanto corporativos

from app.agents.base import BaseAgent

class QAAgent(BaseAgent):
    """
    Agente de Perguntas e Respostas baseado em documentos.
    Responde apenas com base no conteúdo fornecido via RAG.
    """

    def system_prompt(self) -> str:
        return (
            "Você é um assistente especializado em responder perguntas "
            "com base estritra em documentos fornecidos. "
            "Não utilize conhecimento externo."
            "Se a resposxta não estiver presenmte no contexto, "
            "declare explicitamente que a informação não foi encotrada"
        )
    
    def build_prompt(self, query: str, context: str) -> str:
        """
        Constrói o prompt final para Q&A.
        """
        return f"""
CONTEXTO:
{context}

PERGUNTA:
{query}

INTRUÇÕES:
- Responda apenas com base no contexto acima
- Seja claro, direto e objetivo
- Não faça suposições
- Caso a resposta não esteja no documento, responda:
  "A informação solicitada não foi encontrada nos documentos analisados."

RESPOSTA:
"""