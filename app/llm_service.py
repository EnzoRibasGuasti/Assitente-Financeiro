"""Conversão de perguntas em linguagem natural para queries SQL,
usando a API da Anthropic (Claude).

Requer a variável de ambiente ANTHROPIC_API_KEY configurada.
"""

import os
import anthropic

from app.models import TABLE_SCHEMA

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = f"""
You are an assistant that converts natural language questions into
valid SQLite SELECT queries.

Database schema:
{TABLE_SCHEMA}

Rules:
- Only generate SELECT queries. Never generate INSERT, UPDATE, DELETE or DROP.
- Return ONLY the raw SQL query, with no explanation, no markdown, no backticks.
- Dates are in the format YYYY-MM-DD.
- Amounts are in Brazilian Reais (numeric, no currency symbol).
"""


def question_to_sql(question: str) -> str:
    """Envia a pergunta para o modelo e retorna a query SQL gerada.

    Args:
        question: Pergunta em linguagem natural (ex: "quanto gastei
            em mercado esse mês?").

    Returns:
        Query SQL gerada pelo modelo, já sem blocos de markdown.
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )

    sql = response.content[0].text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql
