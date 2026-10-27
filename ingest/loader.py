# S2: load the source PDFs into documents, normalize text, and strip the repeating page footer.
# Uses pypdf directly (one Document per page) rather than langchain-community's PyPDFLoader,
# which is being sunset.
import re
from pathlib import Path

from langchain_core.documents import Document

# S2: boilerplate repeated on every page; left in, it would show up in chunks and answers
FOOTER_PATTERNS = [
    re.compile(r"^OpsVault \(fictional\) - synthetic document for the enterprise-rag portfolio project\s*$", re.M),
    re.compile(r"^Page \d+\s*$", re.M),
]


def clean_text(text: str) -> str:
    for pattern in FOOTER_PATTERNS:
        text = pattern.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)  # S2: collapse runs of spaces pypdf inserts between words
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pdf(path: Path, root: Path) -> list[Document]:
    from pypdf import PdfReader

    docs = []
    for number, page in enumerate(PdfReader(path).pages, start=1):
        text = clean_text(page.extract_text() or "")
        if text:  # S2: skip blank pages so they never become empty chunks
            # S2: source is relative to raw/, so citations read "msa/stratocore-cloud-msa.pdf"
            docs.append(Document(page_content=text, metadata={"source": path.relative_to(root).as_posix(), "page": number}))
    return docs


def load_documents(raw: Path) -> list[Document]:
    if not raw.is_dir():
        raise FileNotFoundError(f"No source folder at {raw}; put the PDFs in data/<use-case>/raw/<type>/")
    docs = []
    for path in sorted(raw.rglob("*.pdf")):
        docs.extend(load_pdf(path, raw))
    return docs
