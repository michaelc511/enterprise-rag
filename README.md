# Enterprise RAG

RAG (Retrieval-Augmented Generation) assistant over enterprise documents — vendor contracts, audit
reports, and compliance policies — giving procurement, security, GRC, and legal teams accurate, cited
answers. Built step by step from the 15-step pipeline in the reference PDF below, plus S16 (web UIs).

**Active use case:** [Vendor Risk & Compliance](use-cases/vendor-risk-compliance.md). The pipeline is
business-agnostic; each use case in `use-cases/` defines its docs, metadata, PII rules, and demo questions.
Not legal advice.

## Files

| File | Purpose |
|---|---|
| `15 Steps in Building Enterprise-Grade AI Agents_ The Complete 15-Step RAG Pipeline Architecture.pdf` | Reference architecture — the 15 steps (S1–S15) this project implements |
| `README.md` | This file |
| `use-cases/vendor-risk-compliance.md` | Active use case: Vendor Risk & Compliance (contracts, audit reports, policies) |

## Pipeline steps

| Step | Name | Status |
|---|---|---|
| S1 | Data Sources | Not started |
| S2 | Document Loading | Not started |
| S3 | Meaningful Chunking | Not started |
| S4 | Metadata Extraction | Not started |
| S5 | Security & PII Sanitization | Not started |
| S6 | Embeddings | Not started |
| S7 | Vector Database | Not started |
| S8 | Query Rewriting | Not started |
| S9 | Hybrid Search | Not started |
| S10 | Reranking | Not started |
| S11 | Context Assembly | Not started |
| S12 | LLM Generation | Not started |
| S13 | Evaluation | Not started |
| S14 | Semantic / Recursive Chunking | Not started |
| S15 | Advanced Evaluation & Observability | Not started |
| S16 | Web Interfaces (FastAPI `/ask` + Gradio / Streamlit UIs for testing) — not in the PDF | Not started |

## Setup

TBA — added with S1/S2.

## Feature toggles

None yet. Toggles are env vars that default to on — set to `false` to turn off.

## Tests & evals

TBA — `pytest` for fully mocked unit tests (`tests/`), real-key checks in `evaluation/`.
