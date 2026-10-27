# Phase 1 glue: build_index() runs S2 -> S3 -> (S4 -> S5) -> S6 -> S7 in order. Not a step itself.
from core import config
from ingest import chunker, loader, vectorstore


def build_index(case: str | None = None, embeddings=None) -> dict:
    raw = config.raw_dir(case)
    docs = loader.load_documents(raw)  # S2
    chunks = chunker.chunk_documents(docs)  # S3
    # S4 metadata and S5 redaction slot in here once built
    if embeddings is None:
        from core.llm import build_embeddings

        embeddings = build_embeddings()  # S6
    path = config.index_dir(case)
    vectorstore.build_index(chunks, embeddings, path)  # S7
    files = len({d.metadata["source"] for d in docs})
    return {"files": files, "pages": len(docs), "chunks": len(chunks), "index": path}
