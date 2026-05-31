from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .chunker import chunk_markdown
from .db import create_db_engine


@dataclass(frozen=True)
class IngestResult:
    document_id: str
    source_path: str
    chunk_count: int


def document_id_for_path(path: Path) -> str:
    return hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:32]


def title_from_markdown(path: Path, content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return path.stem


def iter_markdown_files(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("**/*.md"))
    return [path]


def ingest_markdown_path(path: Path, engine: Engine | None = None) -> list[IngestResult]:
    resolved_engine = engine or create_db_engine()
    results: list[IngestResult] = []

    with resolved_engine.begin() as connection:
        for file in iter_markdown_files(path):
            content = file.read_text(encoding="utf-8")
            document_id = document_id_for_path(file)
            title = title_from_markdown(file, content)
            chunks = chunk_markdown(content)

            connection.execute(
                text(
                    """
                    REPLACE INTO documents (id, title, source_path, source_type)
                    VALUES (:id, :title, :source_path, 'markdown')
                    """
                ),
                {"id": document_id, "title": title, "source_path": str(file)},
            )

            connection.execute(text("DELETE FROM chunks WHERE document_id = :document_id"), {"document_id": document_id})

            for chunk in chunks:
                chunk_id = f"{document_id}-{chunk.index}"
                connection.execute(
                    text(
                        """
                        REPLACE INTO chunks (
                          id, document_id, chunk_index, content, content_hash, embedding, metadata
                        ) VALUES (
                          :id, :document_id, :chunk_index, :content, :content_hash, :embedding, :metadata
                        )
                        """
                    ),
                    {
                        "id": chunk_id,
                        "document_id": document_id,
                        "chunk_index": chunk.index,
                        "content": chunk.content,
                        "content_hash": chunk.content_hash,
                        "embedding": None,
                        "metadata": json.dumps({"source_path": str(file)}, ensure_ascii=False),
                    },
                )

            results.append(IngestResult(document_id=document_id, source_path=str(file), chunk_count=len(chunks)))

    return results
