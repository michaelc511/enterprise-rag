# S7 search now; S9 later upgrades it to hybrid BM25 + vector search.
from langchain_core.documents import Document

TOP_K = 4


def search(index, question: str, k: int = TOP_K) -> list[Document]:
    # S7: embeds the question with the same model as the chunks and returns the k nearest
    return index.similarity_search(question, k=k)
