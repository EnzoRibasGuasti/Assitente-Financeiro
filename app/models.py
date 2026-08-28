"""Schema da tabela e modelos Pydantic usados pela API."""

from pydantic import BaseModel

TABLE_SCHEMA = """
Table: transactions
Columns:
  - id (INTEGER): identificador único
  - date (TEXT): data da transação, formato YYYY-MM-DD
  - category (TEXT): categoria do gasto (ex: mercado, transporte, lazer)
  - amount (REAL): valor da transação em reais
  - description (TEXT): descrição livre da transação
"""


class AskRequest(BaseModel):
    """Corpo da requisição enviada para POST /ask."""

    question: str


class AskResponse(BaseModel):
    """Corpo da resposta retornada por POST /ask."""

    question: str
    sql_generated: str
    result: list[dict]
