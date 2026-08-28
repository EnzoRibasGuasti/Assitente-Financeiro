"""Testes automatizados da API.

Rode com:

    pytest

Os testes que dependem do LLM são pulados automaticamente se a
variável ANTHROPIC_API_KEY não estiver configurada.
"""

import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import run_query

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_query_blocks_non_select():
    """Garante que a proteção contra queries destrutivas funciona."""
    with pytest.raises(ValueError):
        run_query("DROP TABLE transactions")


def test_run_query_allows_select():
    result = run_query("SELECT * FROM transactions LIMIT 1")
    assert isinstance(result, list)


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="Requer ANTHROPIC_API_KEY configurada para chamar o LLM",
)
def test_ask_endpoint_returns_valid_structure():
    response = client.post("/ask", json={"question": "quantas transações existem?"})
    assert response.status_code == 200
    data = response.json()
    assert "sql_generated" in data
    assert "result" in data
