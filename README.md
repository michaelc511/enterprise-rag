# Enterprise RAG

RAG (Retrieval-Augmented Generation) assistant over enterprise documents — vendor contracts, audit
reports, and compliance policies — giving procurement, security, GRC, and legal teams accurate, cited
answers. Built step by step from the 15-step pipeline in the reference PDF below, plus S16 (web UIs).

**Company:** [OpsVault](company/vendor-risk-compliance/opsvault.md), a fictional enterprise workflow
platform (IT, HR, customer service, risk, finance, and supply-chain workflows with AI agents). **Active use case:** [Vendor Risk & Compliance](use-cases/vendor-risk-compliance.md). The pipeline is
business-agnostic; each use case in `use-cases/` defines its docs, metadata, PII rules, and demo questions.
Not legal advice.

## Files

| File | Purpose |
|---|---|
| `15 Steps in Building Enterprise-Grade AI Agents_ The Complete 15-Step RAG Pipeline Architecture.pdf` | Reference architecture — the 15 steps (S1–S15) this project implements |
| `README.md` | This file |
| `features.html` | Full write-up per step (S1–S21), grouped by phase; sections are TBA until each step is built |
| `company/vendor-risk-compliance/opsvault.md` | Fictional company profile: OpsVault's products, key vendors, frameworks |
| `scripts/build_checklist.py` | Converts `checklist.csv` (gitignored source) into `checklist.html` |
| `checklist.html` | Step status table (S1–S21), grouped by phase |
| `tests/` | Mocked unit tests (`pytest`), no API key or network |
| `requirements.txt` | Python dependencies |
| `data/vendor-risk-compliance/` | Source PDFs (`raw/`) and FAISS index (`index/`) for the use case (gitignored) |
| `use-cases/vendor-risk-compliance.md` | Active use case: Vendor Risk & Compliance (contracts, audit reports, policies) |

## Pipeline steps

Steps are grouped into phases in build order. S numbers match the reference PDF, so S14 sits in
Phase 1 next to S3, the chunking it improves. "Adds from restaurant" lists features reused from
`restaurant-ai-platform` (its F numbers), built as part of that step.

### Phase 1 — Ingestion & Indexing (offline, once per doc update)
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S1 | Data Sources | | Done |
| S2 | Document Loading | | Not started |
| S3 | Meaningful Chunking | | Not started |
| S14 | Semantic / Recursive Chunking | | Not started |
| S4 | Metadata Extraction | | Not started |
| S5 | Security & PII Sanitization | | Not started |
| S6 | Embeddings | **F2** LLM & embeddings provider (OpenAI or Azure) in `core/llm.py`; reused by S8, S12, S13 | Not started |
| S7 | Vector Database | **F3** FAISS index cache so docs aren't re-embedded every run | Not started |

### Phase 2 — Pre-retrieval (every query)
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S8 | Query Rewriting (+ query-side redaction) | | Not started |

### Phase 3 — Retrieval
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S9 | Hybrid Search (BM25 + vector) | | Not started |

### Phase 4 — Post-retrieval
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S10 | Reranking | | Not started |
| S11 | Context Assembly | | Not started |

### Phase 5 — Generation  ✅ milestone: working RAG demo in the terminal
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S12 | LLM Generation (+ answer-side redaction check) | | Not started |

### Phase 6 — Evaluation & Observability
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S13 | Evaluation | | Not started |
| S15 | Advanced Evaluation & Observability | **F6** token & cost tracking; **F11** SQLite usage log (audit trail) | Not started |

### Phase 7 — Serving (not in the PDF)
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S16 | Web Interfaces (FastAPI `/ask` + Gradio / Streamlit) | | Not started |

### Phase 8 — Agentic RAG & Production Hardening (not in the PDF)
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S17 | Agentic RAG (LangGraph): multi-step vendor review with tools (`search_contracts`, `search_audit_reports`, `check_policy`, `create_risk_ticket` via a mock Table API), human approval before tickets, saved state | **F13** LangGraph engine; **F16** persistent thread checkpointing | Planned |
| S18 | Prompt-Injection Defense: treat retrieved vendor docs as untrusted data | **F22** | Deferred |
| S19 | Guardrails: off-topic and "not legal advice" checks (`GUARDRAILS_ENABLED`) | **F19** | Deferred |
| S20 | CI Eval Gate: `pytest` + evals on every push | **F20** | Deferred |
| S21 | API Auth & RBAC (optional) | **F21** (not built in restaurant) | Deferred |

## Setup

Create and activate a Python 3.11 venv (from this folder), then install dependencies:

```
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Put the source PDFs in `data/vendor-risk-compliance/raw/<type>/` (11 synthetic PDFs for the active use
case; see the use-case file for the list). `data/` is gitignored, so documents stay local.

## Feature toggles

None yet. Toggles are env vars that default to on — set to `false` to turn off.

## Tests & evals

```
pytest                              # mocked unit tests, no API key or network
python scripts/build_checklist.py   # rebuild checklist.html after editing checklist.csv
```

Real-key checks will live in `evaluation/` (S13).
