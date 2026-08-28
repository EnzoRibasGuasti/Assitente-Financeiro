"""Importa o CSV de transações para o banco SQLite.

Rode este script uma vez antes de subir a API:

    python -m app.import_data
"""

from pathlib import Path

import pandas as pd

from app.database import create_table, get_connection

CSV_PATH = Path(__file__).parent.parent / "data" / "transactions.csv"


def import_csv_to_db() -> None:
    """Lê o CSV de transações e substitui os dados atuais do banco."""
    create_table()

    df = pd.read_csv(CSV_PATH)

    expected_columns = {"date", "category", "amount", "description"}
    if not expected_columns.issubset(df.columns):
        raise ValueError(
            f"CSV está com colunas erradas. Esperado: {expected_columns}, "
            f"encontrado: {set(df.columns)}"
        )

    conn = get_connection()
    conn.execute("DELETE FROM transactions")
    df.to_sql("transactions", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

    print(f"{len(df)} transações importadas com sucesso para o banco.")


if __name__ == "__main__":
    import_csv_to_db()
