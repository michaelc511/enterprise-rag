# S2: loader tests against PDFs generated in tmp_path.
import pytest

from ingest import loader


def test_clean_text_strips_footer_and_extra_spaces() -> None:
    raw = ("7.2   Encryption at rest.\n\n\n\nOpsVault (fictional) - synthetic document for the "
           "enterprise-rag portfolio project\nPage 2\n")
    assert loader.clean_text(raw) == "7.2 Encryption at rest."


def test_load_documents_one_doc_per_page_with_source_and_page(make_pdf, tmp_path) -> None:
    make_pdf("msa/acme-msa.pdf", ["8.1 Notify within 48 hours.", "12.2 Super cap of 2x fees."])
    make_pdf("nda/acme-nda.pdf", ["Mutual NDA."])

    docs = loader.load_documents(tmp_path / "raw")

    assert [(d.metadata["source"], d.metadata["page"]) for d in docs] == [
        ("msa/acme-msa.pdf", 1), ("msa/acme-msa.pdf", 2), ("nda/acme-nda.pdf", 1)]
    assert docs[0].page_content == "8.1 Notify within 48 hours."
    assert all("synthetic document" not in d.page_content for d in docs)


def test_load_documents_skips_blank_pages(make_pdf, tmp_path) -> None:
    make_pdf("sow/blank.pdf", ["Real text.", ""])  # second page holds only the footer
    docs = loader.load_documents(tmp_path / "raw")
    assert len(docs) == 1


def test_load_documents_missing_folder_raises(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="data/<use-case>/raw"):
        loader.load_documents(tmp_path / "nope")
