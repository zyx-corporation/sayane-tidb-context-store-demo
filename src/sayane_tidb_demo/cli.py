from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from .chunker import chunk_markdown

app = typer.Typer(help="Sayane TiDB Context Store Demo CLI")


@app.command()
def init() -> None:
    """Initialize the demo schema."""
    print("[yellow]TODO:[/yellow] initialize TiDB schema from sql/*.sql")


@app.command()
def ingest(path: Path) -> None:
    """Preview Markdown ingestion and chunking."""
    files = sorted(path.glob("**/*.md")) if path.is_dir() else [path]
    for file in files:
        chunks = chunk_markdown(file.read_text(encoding="utf-8"))
        print(f"[green]{file}[/green]: {len(chunks)} chunks")


@app.command()
def search(query: str, mode: str = "hybrid") -> None:
    """Run a search query."""
    print({"query": query, "mode": mode, "status": "TODO"})


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
