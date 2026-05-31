from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from .config import Settings, load_settings


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    embedding: list[float]


class EmbeddingProvider:
    def embed_texts(self, texts: list[str]) -> list[EmbeddingResult]:
        raise NotImplementedError


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or load_settings()
        if not self.settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for embedding generation")
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def embed_texts(self, texts: list[str]) -> list[EmbeddingResult]:
        if not texts:
            return []
        response = self.client.embeddings.create(
            model=self.settings.embedding_model,
            input=texts,
        )
        return [
            EmbeddingResult(text=text, embedding=item.embedding)
            for text, item in zip(texts, response.data, strict=True)
        ]


def create_embedding_provider(settings: Settings | None = None) -> EmbeddingProvider:
    return OpenAIEmbeddingProvider(settings=settings)
