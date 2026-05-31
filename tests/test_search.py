import pytest

from sayane_tidb_demo.search import SearchResult, cosine_similarity, merge_hybrid_results


def result(chunk_id: str, score: float) -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id="doc",
        chunk_index=0,
        content=f"content {chunk_id}",
        score=score,
    )


def test_cosine_similarity_returns_one_for_same_direction() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


def test_cosine_similarity_returns_zero_for_orthogonal_vectors() -> None:
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_similarity_returns_zero_for_dimension_mismatch() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0]) == pytest.approx(0.0)


def test_cosine_similarity_returns_zero_for_empty_vector() -> None:
    assert cosine_similarity([], [1.0]) == pytest.approx(0.0)


def test_merge_hybrid_results_boosts_text_matches() -> None:
    merged = merge_hybrid_results(text_results=[result("text", 1.0)], vector_results=[], limit=5)
    assert merged[0].chunk_id == "text"
    assert merged[0].score == pytest.approx(1.5)


def test_merge_hybrid_results_combines_duplicate_text_and_vector_hits() -> None:
    merged = merge_hybrid_results(
        text_results=[result("same", 1.0)],
        vector_results=[result("same", 0.7)],
        limit=5,
    )
    assert len(merged) == 1
    assert merged[0].chunk_id == "same"
    assert merged[0].score == pytest.approx(2.2)


def test_merge_hybrid_results_respects_limit() -> None:
    merged = merge_hybrid_results(
        text_results=[result("a", 1.0), result("b", 1.0)],
        vector_results=[result("c", 0.9)],
        limit=2,
    )
    assert len(merged) == 2
