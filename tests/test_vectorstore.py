# S7/F3: index build, save, reload, and search, with fake embeddings.
import pytest
from langchain_core.documents import Document

from ingest import vectorstore
from retrieval.search import search

CHUNKS = [
    Document(page_content="Notify within 48 hours.", metadata={"source": "msa/a.pdf", "page": 1}),
    Document(page_content="AES-256 at rest.", metadata={"source": "msa/a.pdf", "page": 2}),
    Document(page_content="Mutual NDA.", metadata={"source": "nda/b.pdf", "page": 1}),
]


def test_build_saves_and_reload_finds_same_chunks(fake_embeddings, tmp_path) -> None:
    vectorstore.build_index(CHUNKS, fake_embeddings, tmp_path / "idx")
    assert (tmp_path / "idx" / "index.faiss").exists()

    reloaded = vectorstore.load_index(fake_embeddings, tmp_path / "idx")
    # DeterministicFakeEmbedding maps identical text to identical vectors, so an exact match ranks first
    top = search(reloaded, "AES-256 at rest.", k=2)
    assert len(top) == 2
    assert top[0].page_content == "AES-256 at rest."
    assert top[0].metadata == {"source": "msa/a.pdf", "page": 2}


def test_load_missing_index_says_run_build(fake_embeddings, tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="rag.py build"):
        vectorstore.load_index(fake_embeddings, tmp_path / "none")


def test_build_with_no_chunks_raises(fake_embeddings, tmp_path) -> None:
    with pytest.raises(ValueError, match="No chunks"):
        vectorstore.build_index([], fake_embeddings, tmp_path / "idx")
