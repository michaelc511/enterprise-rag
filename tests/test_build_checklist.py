# S1: tests for the checklist converter, using a tiny CSV in tmp_path.
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_checklist.py"
HEADER = "Step #,Phase,Step Name,Status,Target Location,Hiring Value\n"


@pytest.fixture
def chk():
    spec = importlib.util.spec_from_file_location("build_checklist", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_groups_rows_under_phase_dividers(chk, tmp_path) -> None:
    src = tmp_path / "checklist.csv"
    src.write_text(HEADER
                   + 'S1,Phase 1 — Ingestion,Data Sources,Done,"scripts/a.py, data/",6 / 10\n'
                   + "S2,Phase 1 — Ingestion,Loading,Not Started,ingest/,6 / 10\n"
                   + "S17,Phase 8 — Agentic,Agentic RAG,Planned,agents/,10 / 10\n")
    out = tmp_path / "checklist.html"

    assert chk.build(src, out) == 3
    page = out.read_text()
    # S1: one divider per phase change, and Phase is not repeated as a column
    assert page.count('class="phase-row"') == 2
    assert "<th>Phase</th>" not in page
    assert '<span class="badge done">Done</span>' in page
    assert '<span class="badge not-started">Not Started</span>' in page
    assert '<span class="badge planned">Planned</span>' in page
    assert "<code>scripts/a.py</code>, <code>data/</code>" in page


def test_cell_escapes_html(chk) -> None:
    assert chk._cell("Step Name", "Security & PII") == "<td>Security &amp; PII</td>"
