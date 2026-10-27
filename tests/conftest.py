# Shared fixtures: fake embeddings and a tiny PDF, so every test runs offline with no API key.
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # tests import core/, ingest/, retrieval/, engines/ from the repo root


@pytest.fixture
def fake_embeddings():
    from langchain_core.embeddings import DeterministicFakeEmbedding

    return DeterministicFakeEmbedding(size=32)


@pytest.fixture
def make_pdf(tmp_path):
    # Writes a one- or multi-page PDF with the real synthetic footer, so the loader's footer
    # stripping is tested against the exact text it will see
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas

    def _make(relative: str, pages: list[str]) -> Path:
        path = tmp_path / "raw" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(path), pagesize=LETTER)
        for number, text in enumerate(pages, start=1):
            y = 720
            for line in text.split("\n"):
                c.drawString(72, y, line)
                y -= 14
            c.drawString(72, 36, "OpsVault (fictional) - synthetic document for the enterprise-rag portfolio project")
            c.drawString(500, 36, f"Page {number}")
            c.showPage()
        c.save()
        return path

    return _make
