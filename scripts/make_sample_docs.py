# S1: builds the synthetic source PDFs for a use case from Markdown sources, so the sample corpus
# is reproducible and every doc can be edited as text instead of by hand in a PDF tool.
#
# Reads  data/<use-case>/source/<folder>/<name>.md
# Writes data/<use-case>/raw/<folder>/<name>.pdf
#
# Usage: python scripts/make_sample_docs.py [use-case]   (default: vendor-risk-compliance)

import re
import sys
from pathlib import Path

DEFAULT_USE_CASE = "vendor-risk-compliance"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
# S1: every page says the doc is fake, so a stray copy can't pass as a real company record
FOOTER_TEXT = "OpsVault (fictional) - synthetic document for the enterprise-rag portfolio project"


def _inline(text: str) -> str:
    # S1: reportlab paragraphs take mini-HTML, so escape first, then restore **bold** and `code`
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)


def _table(rows: list[str], styles: dict):
    from reportlab.lib import colors
    from reportlab.platypus import Paragraph, Table, TableStyle

    # S1: drop the |---| separator row; wrap cells in Paragraphs so long text wraps inside the cell
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-+:?", c) for c in r)]
    data = [[Paragraph(_inline(c), styles["cell"]) for c in r] for r in cells]
    table = Table(data, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def _flowables(markdown: str, styles: dict) -> list:
    from reportlab.platypus import ListFlowable, ListItem, Paragraph, Spacer

    out: list = []
    para: list[str] = []
    bullets: list[str] = []
    numbered: list[str] = []
    table: list[str] = []

    def flush() -> None:
        if para:
            out.append(Paragraph(_inline(" ".join(para)), styles["body"]))
            para.clear()
        for items, kind in ((bullets, "bullet"), (numbered, "1")):
            if items:
                flow = [ListItem(Paragraph(_inline(i), styles["body"])) for i in items]
                out.append(ListFlowable(flow, bulletType=kind, leftIndent=14))
                items.clear()
        if table:
            out.append(_table(table, styles))
            out.append(Spacer(1, 6))
            table.clear()

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            if para or bullets:
                flush()
            table.append(stripped)
            continue
        if table:
            flush()
        if not stripped:
            flush()
        elif stripped.startswith("### "):
            flush()
            out.append(Paragraph(_inline(stripped[4:]), styles["h3"]))
        elif stripped.startswith("## "):
            flush()
            out.append(Paragraph(_inline(stripped[3:]), styles["h2"]))
        elif stripped.startswith("# "):
            flush()
            out.append(Paragraph(_inline(stripped[2:]), styles["h1"]))
        elif stripped.startswith("- "):
            if para or numbered:
                flush()
            bullets.append(stripped[2:])
        elif re.match(r"\d+\.\s", stripped):
            if para or bullets:
                flush()
            numbered.append(re.sub(r"^\d+\.\s+", "", stripped))
        else:
            # S1: a line opening in bold is a field or clause ("**Policy ID:** ...", "**7.2 ...**"),
            # so it starts its own paragraph instead of merging into the previous line
            if stripped.startswith("**") or bullets or numbered:
                flush()
            para.append(stripped)
    flush()
    return out


def _styles() -> dict:
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

    base = getSampleStyleSheet()
    return {
        "h1": base["Title"],
        "h2": base["Heading2"],
        "h3": base["Heading3"],
        "body": ParagraphStyle("body", parent=base["BodyText"], spaceAfter=6, leading=14),
        "cell": ParagraphStyle("cell", parent=base["BodyText"], fontSize=8.5, leading=10.5),
    }


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(doc.leftMargin, 0.5 * 72, FOOTER_TEXT)
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 0.5 * 72, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(source: Path, target: Path) -> None:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.platypus import SimpleDocTemplate

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(target), pagesize=LETTER, title=source.stem, author="OpsVault (fictional)")
    doc.build(_flowables(source.read_text(), _styles()), onFirstPage=_footer, onLaterPages=_footer)


def build_all(use_case: str = DEFAULT_USE_CASE) -> list[Path]:
    source_dir = DATA_DIR / use_case / "source"
    raw_dir = DATA_DIR / use_case / "raw"
    built = []
    for source in sorted(source_dir.rglob("*.md")):
        target = raw_dir / source.relative_to(source_dir).with_suffix(".pdf")
        build_pdf(source, target)
        built.append(target)
    return built


if __name__ == "__main__":
    use_case = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USE_CASE
    for path in build_all(use_case):
        print(path.relative_to(DATA_DIR.parent))
