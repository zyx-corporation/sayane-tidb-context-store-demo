from __future__ import annotations

from dataclasses import dataclass
import hashlib

CHUNKING_STRATEGY = "paragraph-boundary-max-chars-1200"


@dataclass(frozen=True)
class Chunk:
    index: int
    content: str
    content_hash: str


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_markdown(text: str, max_chars: int = 1200) -> list[Chunk]:
    normalized = text.strip()
    if not normalized:
        return []

    paragraphs = [part.strip() for part in normalized.split("\n\n") if part.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for paragraph in paragraphs:
        candidate_len = current_len + len(paragraph) + (2 if current else 0)
        if current and candidate_len > max_chars:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            current_len = len(paragraph)
        else:
            current.append(paragraph)
            current_len = candidate_len

    if current:
        chunks.append("\n\n".join(current))

    return [Chunk(index=i, content=chunk, content_hash=stable_hash(chunk)) for i, chunk in enumerate(chunks)]
