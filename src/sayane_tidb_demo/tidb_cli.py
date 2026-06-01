from __future__ import annotations

import typer
from rich import print

from .config import DatabaseConfigError, validate_tidb_settings
from .db import create_db_engine, ping_database


def require_tidb_config(*, ping: bool = False) -> None:
    """Validate TiDB settings and optionally verify connectivity."""
    try:
        settings = validate_tidb_settings()
    except DatabaseConfigError as exc:
        print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from None

    if not ping:
        return

    if not ping_database(create_db_engine(settings)):
        print(
            "[red]Failed to connect to TiDB.[/red]\n"
            "Check TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DATABASE, and TIDB_SSL_CA."
        )
        raise typer.Exit(code=1)
