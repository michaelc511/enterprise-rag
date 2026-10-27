# S1: converts checklist.csv (gitignored source) into checklist.html (committed), so step status
# is edited in one place and the published table never drifts from it.
#
# Usage: python scripts/build_checklist.py

import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "checklist.csv"
HTML_PATH = ROOT / "checklist.html"
# S1: same badge colors as restaurant-ai-platform's checklist, plus amber for planned/deferred work
BADGES = {"done": "done", "not started": "not-started", "planned": "planned", "deferred": "deferred"}
NUM_COLUMNS = {"Step #", "New .py File?", "Hiring Value"}

STYLE = """
  :root { --bg:#fff; --fg:#1a1a1a; --muted:#6b7280; --border:#e5e7eb; --stripe:#f9fafb;
          --header-bg:#111827; --header-fg:#fff; }
  * { box-sizing: border-box; }
  body { margin:0; padding:2rem; background:var(--bg); color:var(--fg);
         font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  h1 { font-size:1.4rem; margin:0 0 0.25rem; }
  p.subtitle { margin:0 0 1.5rem; color:var(--muted); font-size:0.9rem; }
  .table-wrap { overflow-x:auto; border:1px solid var(--border); border-radius:8px; }
  table { border-collapse:collapse; width:100%; min-width:1200px; font-size:0.85rem; }
  thead th { background:var(--header-bg); color:var(--header-fg); text-align:left;
             padding:0.6rem 0.75rem; position:sticky; top:0; white-space:nowrap; }
  tbody td { padding:0.55rem 0.75rem; border-bottom:1px solid var(--border); vertical-align:top; }
  tbody tr:nth-child(even) { background:var(--stripe); }
  tbody tr:hover { background:#eef2ff; }
  td.num, th.num { text-align:center; white-space:nowrap; }
  td.status { white-space:nowrap; }
  .badge { display:inline-block; padding:0.15rem 0.55rem; border-radius:999px; font-size:0.75rem; font-weight:600; }
  .badge.done { background:#d1fae5; color:#065f46; }
  .badge.not-started { background:#fee2e2; color:#991b1b; }
  .badge.planned, .badge.deferred { background:#fef3c7; color:#92400e; }
  tr.phase-row td { background:var(--header-bg); color:var(--header-fg); font-weight:700;
                    font-size:0.95rem; padding:0.55rem 0.75rem; }
  tr.phase-row td .phase-num { color:#93c5fd; margin-right:0.4rem; }
  code { font-size:0.8rem; background:#f3f4f6; padding:0.1rem 0.3rem; border-radius:4px; }
"""


def _cell(column: str, value: str) -> str:
    text = html.escape(value)
    if column == "Status":
        badge = BADGES.get(value.strip().lower(), "not-started")
        return f'<td class="status"><span class="badge {badge}">{text}</span></td>'
    if column == "Target Location" and value:
        return "<td>" + ", ".join(f"<code>{html.escape(p.strip())}</code>" for p in value.split(",")) + "</td>"
    return f'<td class="num">{text}</td>' if column in NUM_COLUMNS else f"<td>{text}</td>"


def render(rows: list[dict[str, str]]) -> str:
    # S1: Phase is shown as a full-width divider row, not a column, matching the restaurant layout
    columns = [c for c in rows[0] if c != "Phase"] if rows else []
    head = "".join(f'<th class="num">{html.escape(c)}</th>' if c in NUM_COLUMNS else f"<th>{html.escape(c)}</th>"
                   for c in columns)
    body, phase = [], None
    for row in rows:
        if row["Phase"] != phase:
            phase = row["Phase"]
            num, _, title = phase.partition(" — ")
            body.append(f'      <tr class="phase-row"><td colspan="{len(columns)}">'
                        f'<span class="phase-num">{html.escape(num)}</span>{html.escape(title)}</td></tr>')
        body.append("      <tr>" + "".join(_cell(c, row[c]) for c in columns) + "</tr>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Enterprise RAG Step Checklist</title>
<style>{STYLE}</style>
</head>
<body>
  <h1>Enterprise RAG Step Checklist</h1>
  <p class="subtitle">Converted from checklist.csv by scripts/build_checklist.py</p>
  <div class="table-wrap">
  <table>
    <thead><tr>{head}</tr></thead>
    <tbody>
{chr(10).join(body)}
    </tbody>
  </table>
  </div>
</body>
</html>
"""


def build(csv_path: Path = CSV_PATH, html_path: Path = HTML_PATH) -> int:
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    html_path.write_text(render(rows), encoding="utf-8")
    return len(rows)


if __name__ == "__main__":
    print(f"Wrote {build()} rows to {HTML_PATH.name}")
