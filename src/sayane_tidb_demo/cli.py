from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from .capabilities import get_backend_capabilities
from .ingest import ingest_markdown_path
from .schema import initialize_schema
from .search import get_retrieval_log, list_retrieval_logs, run_search
from .tidb_cli import require_tidb_config

app = typer.Typer(help="Sayane TiDB Context Store Demo CLI")


@app.command()
def capabilities() -> None:
    """Show backend capability metadata without requiring TiDB or OpenAI."""
    print(get_backend_capabilities().to_dict())


@app.command()
def init() -> None:
    """Initialize the demo schema."""
    require_tidb_config(ping=True)
    statement_count = initialize_schema()
    print(f"[green]Initialized schema[/green]: {statement_count} statements executed")


@app.command()
def ingest(path: Path, embed: bool = False) -> None:
    """Ingest Markdown files into TiDB."""
    require_tidb_config(ping=True)
    results = ingest_markdown_path(path, embed=embed)
    for result in results:
        print(
            f"[green]{result.source_path}[/green]: "
            f"{result.chunk_count} chunks, {result.embedded_count} embeddings -> {result.document_id}"
        )


@app.command()
def search(query: str, mode: str = "text", limit: int = 5) -> None:
    """Run a search query and record a retrieval log."""
    require_tidb_config(ping=True)
    try:
        record = run_search(query=query, mode=mode, limit=limit)
    except NotImplementedError as exc:
        print(f"[yellow]{exc}[/yellow]")
        raise typer.Exit(code=2)

    print(f"[green]Retrieval ID:[/green] {record.retrieval_id}")
    print(f"[green]Mode:[/green] {record.mode}")
    print(f"[green]Results:[/green] {len(record.results)}")
    for index, result in enumerate(record.results, start=1):
        preview = result.content.replace("\n", " ")[:160]
        print(f"{index}. {result.chunk_id} score={result.score} :: {preview}")
    print({"audit_summary": record.audit_summary})


@app.command()
def logs(limit: int = 20) -> None:
    """Show retrieval logs."""
    require_tidb_config(ping=True)
    for row in list_retrieval_logs(limit=limit):
        print(row)


@app.command()
def inspect(retrieval_id: str) -> None:
    """Inspect one retrieval log."""
    require_tidb_config(ping=True)
    row = get_retrieval_log(retrieval_id)
    if row is None:
        print(f"[red]not found:[/red] {retrieval_id}")
        raise typer.Exit(code=1)
    print(row)


if __name__ == "__main__":
    app()
