from sayane_tidb_demo.chunker import chunk_markdown


def test_chunk_markdown_keeps_small_document_as_one_chunk() -> None:
    text = "# Title\n\nSayane Context Store Interface."
    chunks = chunk_markdown(text, max_chars=1000)
    assert len(chunks) == 1
    assert "Sayane Context Store Interface" in chunks[0].content


def test_chunk_markdown_splits_by_paragraph_boundary() -> None:
    text = "para1\n\npara2\n\npara3"
    chunks = chunk_markdown(text, max_chars=8)
    assert len(chunks) == 3
