from __future__ import annotations

from dataclasses import dataclass
import json
import math
import uuid

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .audit import lightweight_audit
from .db import create_db_engine
from .embeddings import EmbeddingProvider, create_embedding_provider


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


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


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


def search_vector(
    query: str,
    engine: Engine | None = None,
    limit: int = 5,
    embedding_provider: EmbeddingProvider | None = None,
) -> list[SearchResult]:
    resolved_engine = engine or create_db_engine()
    provider = embedding_provider or create_embedding_provider()
    query_embedding = provider.embed_texts([query])[0].embedding

    with resolved_engine.begin() as connection:
        rows = connection.execute(
            text(
                """
                SELECT id, document_id, chunk_index, content, embedding
                FROM chunks
                WHERE embedding IS NOT NULL
                """
            )
        ).mappings().all()

    scored: list[SearchResult] = []
    for row in rows:
        raw_embedding = row["embedding"]
        chunk_embedding = json.loads(raw_embedding) if isinstance(raw_embedding, str) else raw_embedding
        score = cosine_similarity(query_embedding, chunk_embedding)
        scored.append(
            SearchResult(
                chunk_id=str(row["id"]),
                document_id=str(row["document_id"]),
                chunk_index=int(row["chunk_index"]),
                content=str(row["content"]),
                score=score,
            )
        )

    return sorted(scored, key=lambda item: item.score, reverse=True)[:limit]


def search_hybrid(query: str, engine: Engine | None = None, limit: int = 5) -> list[SearchResult]:
    resolved_engine = engine or create_db_engine()
    text_results = search_text(query=query, engine=resolved_engine, limit=limit)
    vector_results = search_vector(query=query, engine=resolved_engine, limit=limit)

    merged: dict[str, SearchResult] = {}
    for result in text_results:
        merged[result.chunk_id] = SearchResult(
            chunk_id=result.chunk_id,
            document_id=result.document_id,
            chunk_index=result.chunk_index,
            content=result.content,
            score=0.5 + result.score,
        )
    for result in vector_results:
        existing = merged.get(result.chunk_id)
        if existing:
            merged[result.chunk_id] = SearchResult(
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                chunk_index=result.chunk_index,
                content=result.content,
                score=existing.score + result.score,
            )
        else:
            merged[result.chunk_id] = result

    return sorted(merged.values(), key=lambda item: item.score, reverse=True)[:limit]


def run_search(query: str, mode: str = "text", engine: Engine | None = None, limit: int = 5) -> RetrievalRecord:
    if mode not in {"text", "vector", "hybrid"}:
        raise ValueError(f"unsupported search mode: {mode}")

    resolved_engine = engine or create_db_engine()
    if mode == "text":
        results = search_text(query=query, engine=resolved_engine, limit=limit)
    elif mode == "vector":
        results = search_vector(query=query, engine=resolved_engine, limit=limit)
    else:
        results = search_hybrid(query=query, engine=resolved_engine, limit=limit)

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
