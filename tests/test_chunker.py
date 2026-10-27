# S3: chunker tests.
from langchain_core.documents import Document

from ingest import chunker


def _clauses(n: int) -> str:
    return "\n\n".join(f"{i}.1 Clause {i} says the provider will do thing number {i} on time." for i in range(1, n + 1))


def test_chunks_respect_size_and_keep_metadata() -> None:
    doc = Document(page_content=_clauses(60), metadata={"source": "msa/a.pdf", "page": 3})
    chunks = chunker.chunk_documents([doc], chunk_size=300, chunk_overlap=50)

    assert len(chunks) > 1
    assert all(len(c.page_content) <= 300 for c in chunks)
    assert all(c.metadata == {"source": "msa/a.pdf", "page": 3} for c in chunks)


def test_short_page_stays_one_chunk() -> None:
    doc = Document(page_content="Mutual NDA. Term: 3 years.", metadata={"source": "nda/a.pdf", "page": 1})
    assert [c.page_content for c in chunker.chunk_documents([doc])] == ["Mutual NDA. Term: 3 years."]


def test_whitespace_only_pages_produce_no_chunks() -> None:
    assert chunker.chunk_documents([Document(page_content="   \n\n ", metadata={})]) == []
