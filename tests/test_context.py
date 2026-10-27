# S11: context assembly tests.
from langchain_core.documents import Document

from retrieval import context

DOCS = [
    Document(page_content="  Notify within 48 hours. ", metadata={"source": "msa/stratocore-cloud-msa.pdf", "page": 3}),
    Document(page_content="Mutual NDA.", metadata={"source": "nda/x.pdf"}),
]


def test_assemble_numbers_sources_in_order() -> None:
    assert context.assemble_context(DOCS) == (
        "[Source 1: stratocore-cloud-msa.pdf, p. 3]\nNotify within 48 hours.\n\n"
        "[Source 2: x.pdf]\nMutual NDA."
    )


def test_sources_match_the_numbers_in_the_context() -> None:
    assert context.sources(DOCS) == [
        {"n": 1, "source": "msa/stratocore-cloud-msa.pdf", "page": 3},
        {"n": 2, "source": "nda/x.pdf", "page": None},
    ]


def test_empty_input() -> None:
    assert context.assemble_context([]) == ""
    assert context.sources([]) == []
