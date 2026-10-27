# S11: join the top chunks into one context block with [Source n] citations.
from pathlib import Path

from langchain_core.documents import Document


def source_label(doc: Document) -> str:
    # S11: "stratocore-cloud-msa.pdf, p. 3" is enough for a reader to find the clause
    name = Path(doc.metadata.get("source", "unknown")).name
    page = doc.metadata.get("page")
    return f"{name}, p. {page}" if page else name


def assemble_context(docs: list[Document]) -> str:
    # S11: numbered blocks so the LLM can cite [Source n] and the reader can match n to a file
    return "\n\n".join(f"[Source {i}: {source_label(d)}]\n{d.page_content.strip()}" for i, d in enumerate(docs, start=1))


def sources(docs: list[Document]) -> list[dict]:
    return [{"n": i, "source": d.metadata.get("source"), "page": d.metadata.get("page")} for i, d in enumerate(docs, start=1)]
