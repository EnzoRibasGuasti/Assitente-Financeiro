"""Ponto de entrada da API FastAPI.

Expõe o endpoint POST /ask, que recebe uma pergunta em linguagem
natural e retorna a resposta consultando o banco de transações.
"""

from fastapi import FastAPI, HTTPException

from app.database import create_table, run_query
from app.llm_service import question_to_sql
from app.models import AskRequest, AskResponse

app = FastAPI(title="Financial Assistant API")


@app.on_event("startup")
def on_startup() -> None:
    """Garante que a tabela existe assim que a API sobe."""
    create_table()


@app.get("/")
def health_check():
    """Endpoint simples para checar se a API está no ar."""
    return {"status": "ok", "message": "Financial Assistant API is running"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """Converte uma pergunta em SQL, executa no banco e retorna o resultado.

    Args:
        request: Corpo da requisição contendo a pergunta em texto livre.

    Returns:
        A pergunta original, a query SQL gerada e o resultado da consulta.

    Raises:
        HTTPException 400: Se a query gerada não for um SELECT válido.
        HTTPException 500: Se ocorrer qualquer outro erro no processamento.
    """
    try:
        sql = question_to_sql(request.question)
        result = run_query(sql)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar pergunta: {e}")

    return AskResponse(question=request.question, sql_generated=sql, result=result)
