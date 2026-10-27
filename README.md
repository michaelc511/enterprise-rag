# Enterprise RAG

RAG (Retrieval-Augmented Generation) assistant over enterprise documents — vendor contracts, audit
reports, and compliance policies — giving procurement, security, GRC, and legal teams accurate, cited
answers. Built step by step from the 15-step pipeline in the reference PDF below, plus S16 (web UIs).

**Company:** [OpsVault](company/vendor-risk-compliance/opsvault.md), a fictional enterprise workflow
platform (IT, HR, customer service, risk, finance, and supply-chain workflows with AI agents). **Active use case:** [Vendor Risk & Compliance](use-cases/vendor-risk-compliance.md). The pipeline is
business-agnostic; each use case in `use-cases/` defines its docs, metadata, PII rules, and demo questions.
Not legal advice.

## Project structure

One file per job. `(scaffold)` files hold only a header comment until their step is built. The
basic `ask` path (S2, S3, S6, S7, S11, S12) is built. Steps are
listed in [Pipeline steps](#pipeline-steps); `features.html` has the full write-up for each.

```
enterprise-rag/
├── rag.py                     Main entry point: build | ask | chat (serve, eval: later)
├── engine_api.py              S16  FastAPI POST /ask, calls the same engine as `rag.py ask` (scaffold)
│
├── core/                      Shared
│   ├── config.py                   Use case, data/index paths, env toggles
│   └── llm.py                 S6   LLM + embeddings provider, OpenAI or Azure (+F2)
│
├── ingest/                    Phase 1, offline: builds the index
│   ├── loader.py              S2   Load PDFs, clean text
│   ├── chunker.py             S3   Chunk by size; S14 adds clause-aware splitting
│   ├── metadata.py            S4   Doc type, vendor, parties, dates (scaffold)
│   ├── redact.py              S5   PII/secrets redaction; reused for query + answer (scaffold)
│   ├── vectorstore.py         S7   FAISS build/save/load, cached per use case (+F3)
│   └── pipeline.py                 Glue: runs S2 → S7 in order
│
├── retrieval/                 Phases 2–4: runs per question
│   ├── query.py               S8   Query rewriting (scaffold)
│   ├── search.py              S7   Vector search (top 4); S9 upgrades to hybrid BM25 + vector
│   ├── rerank.py              S10  Cross-encoder reranking (scaffold)
│   └── context.py             S11  Context with [Source n] citations
│
├── engines/                   Answer engines, switchable
│   ├── base.py                     Engine interface + get_engine() factory (+F12)
│   ├── plain_rag_engine.py    S12  Retrieve → context → grounded, cited answer
│   └── langgraph_engine.py    S17  Agentic multi-step vendor review (+F13) (scaffold)
│
├── evaluation/                S13, S15: real-API-key checks only
│   ├── run_evals.py                Run test questions through the engine (scaffold)
│   └── scoring.py                  LLM-as-judge + answer-key checks (scaffold)
│
├── web-demo/                  S16: UIs that call engine_api.py
│   ├── gradio_app.py               (scaffold)
│   └── streamlit_app.py            (scaffold)
│
├── tests/                     Mocked unit tests (pytest), no API key or network; conftest.py has fakes
├── scripts/
│   └── build_checklist.py          checklist.csv → checklist.html
│
├── company/vendor-risk-compliance/opsvault.md   Fictional company: what OpsVault does, sells, buys
├── use-cases/vendor-risk-compliance.md          Active use case: docs, PII rules, demo questions
├── data/vendor-risk-compliance/                 (gitignored)
│   ├── raw/                        11 source PDFs: policy, msa, sow, nda, audit-report, questionnaire
│   └── index/                      FAISS index (S7)
│
├── blogs/                     One HTML post per category
│   └── 0-introduction.html         OpsVault, its vendor-risk pain points, and how S1–S21 address them
│
├── blogs/                     Posts: 0-introduction.html, blog1.html
├── features.html              Full write-up per step (S1–S21), grouped by phase
├── checklist.html             Step status table, generated from checklist.csv (gitignored)
├── requirements.txt           Python dependencies (pinned)
├── .env.example               Copy to .env (gitignored) and set OPENAI_API_KEY
├── README.md                  This file
└── 15 Steps in Building Enterprise-Grade AI Agents_ ... .pdf   Reference architecture (S1–S15)
```

To add later: `api/` MCP server (S17), `images/`.

## Pipeline steps

Steps are grouped into phases in build order. S numbers match the reference PDF, so S14 sits in
Phase 1 next to S3, the chunking it improves. "Adds from restaurant" lists features reused from
`restaurant-ai-platform` (its F numbers), built as part of that step.

### Phase 1 — Ingestion & Indexing (offline, once per doc update)
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S1 | Data Sources | | Done |
| S2 | Document Loading | | Done |
| S3 | Meaningful Chunking | | Done |
| S14 | Semantic / Recursive Chunking | | Not started |
| S4 | Metadata Extraction | | Not started |
| S5 | Security & PII Sanitization | | Not started |
| S6 | Embeddings | **F2** LLM & embeddings provider (OpenAI or Azure) in `core/llm.py`; reused by S8, S12, S13 | Done |
| S7 | Vector Database | **F3** FAISS index cache so docs aren't re-embedded every run | Done |

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
| S11 | Context Assembly | | Done |

### Phase 5 — Generation  ✅ milestone: working RAG demo in the terminal
| Step | Name | Adds from restaurant | Status |
|---|---|---|---|
| S12 | LLM Generation (+ answer-side redaction check) | | Done (basic; the redaction check arrives with S5) |

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

Add your API key: copy `.env.example` to `.env` (gitignored) and set `OPENAI_API_KEY`
(or the Azure settings).

Put the source PDFs in `data/vendor-risk-compliance/raw/<type>/` (11 synthetic PDFs for the active use
case; see the use-case file for the list). `data/` is gitignored, so documents stay local.

## Usage

```
python rag.py build                 # S2 → S3 → S6 → S7: load, chunk, embed, save the FAISS index
python rag.py ask "What's the breach notification window in the Stratocore MSA?"
python rag.py chat                  # ask questions in a loop; q to quit
```

Run `build` once, and again whenever the PDFs change; `ask` and `chat` load the saved index. Answers cite
`[Source n]` and list each source file and page. `serve` (S16) and `eval` (S13) aren't built yet.

## Feature toggles

Set in `.env`. Toggles default to on — set to `false` to turn off. None yet.

| Setting | Default | Effect |
|---|---|---|
| `USE_CASE` | `vendor-risk-compliance` | Which `data/<use-case>/` folder to load and index |
| `LLM_MODEL` | `gpt-4o-mini` | Chat model for answers (S12) |
| `EMBEDDINGS_MODEL` | `text-embedding-3-small` | Embeddings model (S6); each model gets its own index folder |

## Tests & evals

```
pytest                              # mocked unit tests, no API key or network
python scripts/build_checklist.py   # rebuild checklist.html after editing checklist.csv
```

Real-key checks will live in `evaluation/` (S13).
