from __future__ import annotations

from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .db import create_db_engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = PROJECT_ROOT / "sql"


def iter_sql_files(sql_dir: Path = SQL_DIR) -> list[Path]:
    return sorted(sql_dir.glob("*.sql"))


def split_sql_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        current.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(current).strip().rstrip(";")
            if statement:
                statements.append(statement)
            current = []
    if current:
        statement = "\n".join(current).strip().rstrip(";")
        if statement:
            statements.append(statement)
    return statements


def initialize_schema(engine: Engine | None = None, sql_dir: Path = SQL_DIR) -> int:
    resolved_engine = engine or create_db_engine()
    count = 0
    with resolved_engine.begin() as connection:
        for sql_file in iter_sql_files(sql_dir):
            for statement in split_sql_statements(sql_file.read_text(encoding="utf-8")):
                connection.execute(text(statement))
                count += 1
    return count
