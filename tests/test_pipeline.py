# Phase 1 glue: build_index() end to end on generated PDFs with fake embeddings.
from core import config
from ingest import pipeline


def test_build_index_runs_load_chunk_embed_store(make_pdf, tmp_path, fake_embeddings, monkeypatch) -> None:
    make_pdf("msa/acme-msa.pdf", ["8.1 Notify within 48 hours.", "12.2 Super cap of 2x fees."])
    make_pdf("nda/acme-nda.pdf", ["Mutual NDA."])
    monkeypatch.setattr(config, "raw_dir", lambda case=None: tmp_path / "raw")
    monkeypatch.setattr(config, "index_dir", lambda case=None, embeddings_model=None: tmp_path / "index")

    stats = pipeline.build_index(embeddings=fake_embeddings)

    assert stats == {"files": 2, "pages": 3, "chunks": 3, "index": tmp_path / "index"}
    assert (tmp_path / "index" / "index.faiss").exists()
