from __future__ import annotations

from dataclasses import dataclass
import json
import uuid

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .audit import lightweight_audit
from .db import create_db_engine


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    score: float


@dataclass(frozen=True)
class RetrievalRecord:
    retrieval_id: str
    query: str
    mode: str
    results: list[SearchResult]
    audit_summary: dict[str, object]


def search_text(query: str, engine: Engine | None = None, limit: int = 5) -> list[SearchResult]:
    resolved_engine = engine or create_db_engine()
    like_query = f"%{query}%"
    tokens = [token for token in query.split() if token]

    with resolved_engine.begin() as connection:
        rows = connection.execute(
            text(
                """
                SELECT id, document_id, chunk_index, content
                FROM chunks
                WHERE content LIKE :like_query
                ORDER BY document_id, chunk_index
                LIMIT :limit
                """
            ),
            {"like_query": like_query, "limit": limit},
        ).mappings().all()

        if not rows and tokens:
            clauses = []
            params: dict[str, object] = {"limit": limit}
            for index, token in enumerate(tokens):
                key = f"token_{index}"
                clauses.append(f"content LIKE :{key}")
                params[key] = f"%{token}%"
            rows = connection.execute(
                text(
                    f"""
                    SELECT id, document_id, chunk_index, content
                    FROM chunks
                    WHERE {' OR '.join(clauses)}
                    ORDER BY document_id, chunk_index
                    LIMIT :limit
                    """
                ),
                params,
            ).mappings().all()

    return [
        SearchResult(
            chunk_id=str(row["id"]),
            document_id=str(row["document_id"]),
            chunk_index=int(row["chunk_index"]),
            content=str(row["content"]),
            score=1.0,
        )
        for row in rows
    ]


def run_search(query: str, mode: str = "text", engine: Engine | None = None, limit: int = 5) -> RetrievalRecord:
    if mode not in {"text", "vector", "hybrid"}:
        raise ValueError(f"unsupported search mode: {mode}")
    if mode != "text":
        raise NotImplementedError(f"{mode} search is not implemented yet")

    resolved_engine = engine or create_db_engine()
    results = search_text(query=query, engine=resolved_engine, limit=limit)
    selected_chunks = [{"id": result.chunk_id, "content": result.content} for result in results]
    audit_summary = lightweight_audit(query, selected_chunks)
    retrieval_id = str(uuid.uuid4())

    with resolved_engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO retrieval_logs (
                  id, query, mode, retrieved_chunk_ids, scores, selected_chunk_ids, audit_summary
                ) VALUES (
                  :id, :query, :mode, :retrieved_chunk_ids, :scores, :selected_chunk_ids, :audit_summary
                )
                """
            ),
            {
                "id": retrieval_id,
                "query": query,
                "mode": mode,
                "retrieved_chunk_ids": json.dumps([result.chunk_id for result in results]),
                "scores": json.dumps({result.chunk_id: result.score for result in results}),
                "selected_chunk_ids": json.dumps([result.chunk_id for result in results]),
                "audit_summary": json.dumps(audit_summary, ensure_ascii=False),
            },
        )

    return RetrievalRecord(
        retrieval_id=retrieval_id,
        query=query,
        mode=mode,
        results=results,
        audit_summary=audit_summary,
    )


def list_retrieval_logs(engine: Engine | None = None, limit: int = 20) -> list[dict[str, object]]:
    resolved_engine = engine or create_db_engine()
    with resolved_engine.begin() as connection:
        rows = connection.execute(
            text(
                """
                SELECT id, query, mode, retrieved_chunk_ids, audit_summary, created_at
                FROM retrieval_logs
                ORDER BY created_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings().all()
    return [dict(row) for row in rows]


def get_retrieval_log(retrieval_id: str, engine: Engine | None = None) -> dict[str, object] | None:
    resolved_engine = engine or create_db_engine()
    with resolved_engine.begin() as connection:
        row = connection.execute(
            text(
                """
                SELECT id, query, mode, retrieved_chunk_ids, scores, selected_chunk_ids, audit_summary, created_at
                FROM retrieval_logs
                WHERE id = :id
                """
            ),
            {"id": retrieval_id},
        ).mappings().first()
    return dict(row) if row else None
