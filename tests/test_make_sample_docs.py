# S1: tests for the sample-doc generator. Runs reportlab locally into tmp_path, so no API key,
# network, or real data/ files are touched.
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "make_sample_docs.py"


@pytest.fixture
def gen():
    # S1: scripts/ isn't a package, so load the module straight from its file path
    spec = importlib.util.spec_from_file_location("make_sample_docs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_inline_escapes_html_then_restores_bold_and_code(gen) -> None:
    out = gen._inline("**Fees** < $5,000 & `ovk_live_x`")
    assert out == '<b>Fees</b> &lt; $5,000 &amp; <font face="Courier">ovk_live_x</font>'


def test_flowables_splits_headings_fields_lists_and_tables(gen) -> None:
    from reportlab.platypus import ListFlowable, Paragraph, Table

    md = "\n".join([
        "# Title",
        "**Policy ID:** POL-1",
        "**Version:** 3.2",
        "- bullet one",
        "1. step one",
        "| A | B |",
        "|---|---|",
        "| x | y |",
        "plain text",
    ])
    out = gen._flowables(md, gen._styles())
    kinds = [type(f).__name__ for f in out]
    # S1: each bold field line stays its own paragraph instead of merging into one run-on line
    assert kinds[:3] == ["Paragraph", "Paragraph", "Paragraph"]
    assert sum(isinstance(f, ListFlowable) for f in out) == 2
    tables = [f for f in out if isinstance(f, Table)]
    assert len(tables) == 1
    assert len(tables[0]._cellvalues) == 2  # separator row dropped
    assert isinstance(out[-1], Paragraph)


def test_build_all_mirrors_source_folders_into_raw(gen, tmp_path, monkeypatch) -> None:
    source = tmp_path / "demo" / "source" / "msa"
    source.mkdir(parents=True)
    (source / "acme-msa.md").write_text("# MSA\n\n**Agreement No.:** MSA-1\n\nBody text.")
    monkeypatch.setattr(gen, "DATA_DIR", tmp_path)

    built = gen.build_all("demo")

    assert built == [tmp_path / "demo" / "raw" / "msa" / "acme-msa.pdf"]
    assert built[0].read_bytes().startswith(b"%PDF")


def test_build_all_with_no_sources_builds_nothing(gen, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(gen, "DATA_DIR", tmp_path)
    assert gen.build_all("missing-use-case") == []
