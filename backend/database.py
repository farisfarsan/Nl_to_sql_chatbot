import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "chatbot")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin123")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def get_schema() -> str:
    """Fetch all table schemas from the database for LangChain context."""
    schema_info = []
    with engine.connect() as conn:
        # Get all tables
        tables = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)).fetchall()

        for (table_name,) in tables:
            # Get columns for each table
            columns = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = :table
                ORDER BY ordinal_position
            """), {"table": table_name}).fetchall()

            col_info = ", ".join([f"{col} ({dtype})" for col, dtype in columns])
            schema_info.append(f"Table: {table_name}\nColumns: {col_info}")

    return "\n\n".join(schema_info)


def run_query(sql: str) -> list:
    """Execute a SQL query and return results as a list of dicts."""
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
