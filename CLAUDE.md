# Enterprise RAG

RAG assistant over internal enterprise docs (policy manuals, technical specs, compliance PDFs) for
engineering and support teams. Built from the 15-step pipeline in
`15 Steps in Building Enterprise-Grade AI Agents_ The Complete 15-Step RAG Pipeline Architecture.pdf`;
features are numbered S1–S15 to match its steps.

## Git & authorship
- Mike Chang is the sole author. Never add a `Co-Authored-By` trailer or any Claude/AI attribution
  to commits, PRs, or files.
- Work on a branch, then merge to `main`. Push to GitHub only when asked.
- Commit only files the task touched — leave unrelated untracked files alone.
- Run `pytest` before committing; all tests must pass.

## Accuracy
- Verify every claim against the source code before stating it — in answers and docs.
- Never invent step numbers (there is no "S7.1").
- Doc examples must use real content from the source docs in `data/raw/`.

## Code conventions
- Tag code with `# S<n>` comments.
- Feature toggles are env vars defaulting to on.
- Unit tests in `tests/` are fully mocked — no API key or network.

## Python style
- PEP 8 naming; `_private` helpers; module constants in UPPER_CASE.
- Type hints on all new function parameters and return values.
- Each new module starts with a `# S<n>: <what and why>` header comment.
- Prefer inline `# S<n>: why` comments over docstrings; explain *why*, not *what*.
- Lazy-import optional/heavy dependencies inside the function that needs them.

## Finishing a step (all in one commit)
1. Code tagged `# S<n>`; mocked tests in `tests/test_<module>.py`; `pytest` passes. Checks that
   need a real API key go in `evaluation/`, never `tests/`.
   - New third-party import → add the package to `requirements.txt`.
   - New on/off toggle → env var defaulting to on.
2. `README.md`: add a Files-table row per new file; add any new env var to "Feature toggles";
   document any new endpoint or command.

## Answer style
- For yes/no questions, lead with **Y** or **N**, then a short explanation.
- Grade reviews A–F with a concrete list of fixes.
- Keep answers short; no padding.
