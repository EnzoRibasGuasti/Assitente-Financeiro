"""Conexão com o banco SQLite e execução segura de queries."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "finance.db"


def get_connection() -> sqlite3.Connection:
    """Abre uma conexão com o banco SQLite.

    Returns:
        Conexão com row_factory configurado para retornar
        linhas acessíveis por nome de coluna (ex: row["amount"]).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table() -> None:
    """Cria a tabela `transactions` caso ela ainda não exista."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def run_query(sql: str) -> list[dict]:
    """Executa uma query SQL de leitura e retorna o resultado.

    Por segurança, só aceita queries que comecem com SELECT. Isso é
    essencial porque a query pode ter sido gerada por um LLM a partir
    de texto livre do usuário, e não devemos confiar cegamente nela.

    Args:
        sql: Query SQL a ser executada.

    Returns:
        Lista de dicionários, um por linha retornada.

    Raises:
        ValueError: Se a query não começar com SELECT.
    """
    sql_clean = sql.strip().rstrip(";")

    if not sql_clean.lower().startswith("select"):
        raise ValueError("Apenas queries SELECT são permitidas por segurança.")

    conn = get_connection()
    try:
        cursor = conn.execute(sql_clean)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
