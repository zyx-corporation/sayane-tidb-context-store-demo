import pytest

from sayane_tidb_demo.search import cosine_similarity


def test_cosine_similarity_returns_one_for_same_direction() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


def test_cosine_similarity_returns_zero_for_orthogonal_vectors() -> None:
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_similarity_returns_zero_for_dimension_mismatch() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0]) == pytest.approx(0.0)


def test_cosine_similarity_returns_zero_for_empty_vector() -> None:
    assert cosine_similarity([], [1.0]) == pytest.approx(0.0)
