# Use Case: Vendor Risk & Compliance Assistant

**Status:** Active use case.

## Business summary
- **What it is:** A RAG assistant for third-party risk management (TPRM). It ingests, secures, indexes,
  and retrieves vendor contracts, vendor audit reports, and internal compliance frameworks and policies.
- **Core value:** Procurement, security, GRC (governance, risk & compliance), and legal teams get cited
  answers about high-stakes contracts and compliance requirements. Governance comes from PII
  redaction, grounded answers, and automated evaluation guards.
- **Disclaimer:** Not legal advice. The answer prompt and the README both say so.

## Source documents (`data/raw/`, gitignored)

| Type | Count | Source |
|---|---|---|
| Master Services Agreements (MSAs) | 2 | Public templates or SEC EDGAR exhibits |
| Non-Disclosure Agreements (NDAs) | 2 | Public templates |
| Statements of Work (SOWs) | 2 | Written to reference one of the MSAs |
| Compliance frameworks & policy manuals | 2 | NIST 800-53 / CIS Controls excerpt + an internal-style security policy |
| Vendor & third-party audit reports | 2 | **Synthetic** (real SOC 2 reports are confidential), labeled as synthetic |

Link the docs together so cross-document questions work. Both SOWs reference one MSA, and at least
one audit report covers a vendor named in a contract.

## PII protection (three layers)
**Redact people, not companies.**
- **Personal data of any individual** (customer, employee, signatory, auditor, notice contact): names,
  signatures, emails, phone numbers, home addresses, government IDs.
- **Secrets and financial data:** bank account and routing numbers, payment card numbers, API keys,
  passwords.
- **Keep:** vendor, company, and contract-party names, business addresses, and contract terms, so
  metadata (S4) and questions like "the Acme MSA" still work.

**How:**
- **Typed placeholders, not blanks:** `[PERSON_1]`, `[EMAIL_2]`, `[BANK_ACCOUNT_1]`, numbered per
  document so answers stay readable ("signed by [PERSON_1]").
- **Detection:** Microsoft Presidio (NER) for names, locations, and IDs, plus regex for card numbers,
  bank numbers, and keys.
- **Redaction log:** per chunk, record the entity type and count, never the original value. This is the
  audit trail.

**Layers:**
1. **Ingestion (S5):** redact before embedding or storage.
2. **Query (S8):** redact the user's question before it reaches the LLM.
3. **Answer (S12):** check the final answer before returning it.

## How each step applies

| Step | Use in this business |
|---|---|
| S1–S2 | Load the 10 PDFs |
| S3, S14 | Chunk by clause and section so clauses aren't split |
| S4 | Metadata: doc type, vendor, parties, effective date, framework |
| S5 | PII and secrets redaction at ingestion (Presidio + regex, typed placeholders, redaction log) |
| S6–S7 | Embeddings + FAISS |
| S8 | Query rewriting + query-side redaction |
| S9 | Hybrid search: BM25 catches "Section 8.2", control IDs like "CC6.1", dollar caps |
| S10 | Cross-encoder reranking puts the exact clause first |
| S11–S12 | Answers cite the doc and clause; answer-side redaction check |
| S13, S15 | Faithfulness evals + LangSmith tracing (audit trail) |
| S16 | Gradio / Streamlit demo UIs |

## Demo questions
- "What's the liability cap in the Acme MSA?" (single contract, exact number)
- "Which SOWs fall under the Acme MSA?" (metadata / cross-reference)
- "What does our policy require for access reviews?" (internal policy)
- "Acme's MSA requires encryption at rest. Does their audit report confirm it, and does that meet our policy?"
  (cross-document, the showcase question)
