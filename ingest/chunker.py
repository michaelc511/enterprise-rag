# S3: split documents into chunks by size. S14 later adds clause-aware splitting here.
from langchain_core.documents import Document

# S3: ~1000 characters holds one or two contract clauses; the overlap keeps a clause that
# straddles a boundary readable in at least one chunk
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def chunk_documents(docs: list[Document], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list[Document]:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    # S3: split_documents copies each page's metadata (source, page) onto every chunk from it
    return [c for c in splitter.split_documents(docs) if c.page_content.strip()]
