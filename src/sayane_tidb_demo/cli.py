from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from .db import ping_database
from .ingest import ingest_markdown_path
from .schema import initialize_schema

app = typer.Typer(help="Sayane TiDB Context Store Demo CLI")


@app.command()
def init() -> None:
    """Initialize the demo schema."""
    if not ping_database():
        raise typer.Exit(code=1)
    statement_count = initialize_schema()
    print(f"[green]Initialized schema[/green]: {statement_count} statements executed")


@app.command()
def ingest(path: Path) -> None:
    """Ingest Markdown files into TiDB."""
    results = ingest_markdown_path(path)
    for result in results:
        print(f"[green]{result.source_path}[/green]: {result.chunk_count} chunks -> {result.document_id}")


@app.command()
def search(query: str, mode: str = "hybrid") -> None:
    """Run a search query."""
    print({"query": query, "mode": mode, "status": "TODO: implement text/vector/hybrid search"})


@app.command()
def logs() -> None:
    """Show retrieval logs."""
    print("[yellow]TODO:[/yellow] show retrieval logs")


@app.command()
def inspect(retrieval_id: str) -> None:
    """Inspect one retrieval log."""
    print({"retrieval_id": retrieval_id, "status": "TODO"})


if __name__ == "__main__":
    app()
