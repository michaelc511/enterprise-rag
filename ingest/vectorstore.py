# S7/F3: build, save, and load the FAISS index per use case, so docs aren't re-embedded every run.
from pathlib import Path

from langchain_core.documents import Document


def build_index(chunks: list[Document], embeddings, path: Path):
    from langchain_community.vectorstores import FAISS

    if not chunks:
        raise ValueError("No chunks to index; check that data/<use-case>/raw/ has PDFs")
    # S6: from_documents is where every chunk is sent to the embeddings model
    index = FAISS.from_documents(chunks, embeddings)
    path.mkdir(parents=True, exist_ok=True)
    index.save_local(str(path))
    return index


def load_index(embeddings, path: Path):
    from langchain_community.vectorstores import FAISS

    if not (path / "index.faiss").exists():
        raise FileNotFoundError(f"No index at {path}; run `python rag.py build` first")
    # F3: the index is a pickle written by our own build step, never downloaded, so loading it is safe
    return FAISS.load_local(str(path), embeddings, allow_dangerous_deserialization=True)
