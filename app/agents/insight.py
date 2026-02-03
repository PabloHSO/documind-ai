# Esse agente será responsável por:
# - Analisar documentos de forma crítica
# - Extrair (Riscos | Oportunidades | Pontos de atenção | Recomendações Práticas)
# Ser útil tanto para: documentos técnicos quanto corporativos

from app.agents.base import BaseAgent

class InsightAgente(BaseAgent):
    """
    Agente responsável por extrair insights estratégicos a partir de documentos.
    Ideal para análises executivas, técnicas e corporativas.
    """

    def system_prompt(self) -> str:
        return(
            "Você é um analista sênior especializado em avaliação de documentos "
            "corporativos e técnicos. Seu objetivo é extrair insights estratégicos, "
            "identificar riscos, oportunidades e recomendações práticas, "
            "sempre com base estrita no conteúdo fornecido."
        ) 
    
    def build_prompt(self, context: str) -> str:
        """
        Constrói o prompt final para geração de insights.
        """

        return f"""

CONTEXTO ANALISADO:
{context}

TAREFA:
Análise o documento acima e gere um relatório estruturado contendo:

1. RESUMO EXECUTIVO
- Síntese clara do conteúdo em até 5 linhas

2. RISCOS INDENTIFICADOS
- Pontos que podem gerar problemas técnicos, legais ou operacionais

3. OPORTUNIDADES
- Melhorias, otimizações e vantagens competitivas possíveis

4. PONTOS DE ATENÇÃO
- Aspectos que exigem cuidado ou acompanhamento

5. RECOMENDAÇÕES
- Ações práticas e objeticas baseadas no documento

REGRAS:
- Não utilize conhecimento externo
- Não faça suposições
- Se alguma seção não tiver informações suficientes, declare explicitamente
- Linguagem profissional e clara

RELATÓRIO:
"""