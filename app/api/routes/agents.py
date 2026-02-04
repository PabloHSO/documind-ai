# Rota para:
# Fazer perguntas (Q&A) sobre documentos indexados
# Gerar resumo executivo
# Manter endpoints claros e versionáveis

from fastapi import APIRouter, HTTPException

from app.api.schemas.agents_schema import QuestionRequest, AgentResponse
from app.agents.summarizer import SummarizerAgent
from app.agents.qa import QAAgent
from app.agents.insight import InsightAgent


router = APIRouter(prefix="/agents", tags=["Agents"])

# =====================
# Endpoints
# =====================

@router.post("/summary", response_model=AgentResponse)
def summaruze_document():
    """
    Gera um resumo executivo dos documentos indexados.
    Ideal para leitura rápida por gestores.
    """

    try:
        agent = SummarizerAgent()
        result = agent.run()

        return {"response": result}
    
    except Exception as e:
        raise HTTPException(
            status_code = 400,
            detail = f"Erro ao gerar resumo: {str(e)}"
        )
    
@router.post("/qa", response_model=AgentResponse)
def question_answering(payload: QuestionRequest):
    """
    Responde perguntas com base nos documentos processados.
    """

    try:
        agent = QAAgent()
        result = agent.run(question = payload.question)

        return {"response": result}
    
    except Exception as e: 
        raise HTTPException(
            status_code=500,
            detail = f"Erro ao responser pergunta: {str(e)}"
        )

@router.post("/insights", response_model=AgentResponse)
def generate_insights():
    """
    Extrai insights estratégicos dos documentos.
    Ex: riscos, oportunidades, padrões e alertas.
    """

    try:
        agent = InsightAgent()
        result = agent.run()

        return {"response": result}
    
    except Exception as e: 
        raise HTTPException(
            status_code=500,
            detail = f"Erro ao gerar Insights: {str(e)}"
        )


