from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError

from .config import Settings, validate_tidb_settings


def create_db_engine(settings: Settings | None = None) -> Engine:
    resolved = validate_tidb_settings(settings)
    connect_args = {}
    if resolved.tidb_ssl_ca:
        connect_args["ssl"] = {"ca": resolved.tidb_ssl_ca}
    return create_engine(resolved.sqlalchemy_url, pool_pre_ping=True, connect_args=connect_args)


@contextmanager
def db_connection(engine: Engine | None = None) -> Iterator[Connection]:
    resolved_engine = engine or create_db_engine()
    with resolved_engine.begin() as connection:
        yield connection


def ping_database(engine: Engine | None = None) -> bool:
    try:
        with db_connection(engine) as connection:
            result = connection.execute(text("SELECT 1"))
            return result.scalar_one() == 1
    except SQLAlchemyError:
        return False
