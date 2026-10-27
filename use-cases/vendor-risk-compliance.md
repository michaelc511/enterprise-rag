# Use Case: Vendor Risk & Compliance Assistant

**Status:** Active use case.

**Company:** OpsVault (fictional). See `company/vendor-risk-compliance/opsvault.md` for its products,
vendors, and frameworks.

## Business summary
- **What it is:** A RAG assistant for third-party risk management (TPRM), shipped as an OpsVault AI
  skill in OpsVault Risk & Compliance (vendor risk) and OpsVault Supply Chain (supplier onboarding).
  It ingests, secures, indexes, and retrieves vendor contracts, vendor audit reports, and OpsVault's
  own compliance policies.
- **Core value:** Procurement, security, GRC, legal, and sales teams get cited answers about
  high-stakes contracts and compliance requirements. Governance comes from PII redaction, grounded
  answers, and automated evaluation guards.
- **Disclaimer:** Not legal advice. The answer prompt and the README both say so.

## Two stages (Customer Zero)
1. **Internal first:** OpsVault's own teams use it to review their vendors and answer their customers.
2. **Then customers:** sold to OpsVault customers inside Risk & Compliance. Each gap found becomes a
   risk ticket (planned agent step, via a mock OpsVault Table API).

## Two directions
- **Inbound (vendor review):** "Is this vendor safe?" Check a vendor's MSA and SOC 2 report against
  OpsVault's policy and flag gaps.
- **Outbound (security questionnaires):** "Prove we're safe." Answer customers' security
  questionnaires with citations from OpsVault's own policies and SOC 2 report.

## Source documents (`data/vendor-risk-compliance/raw/`, gitignored)

All synthetic for now, written as OpsVault documents. Real CUAD contracts can be swapped in later
before the labeled evals (CUAD has no NDAs).

| Folder | Type | Count | Notes |
|---|---|---|---|
| `msa/` | Master Services Agreements | 2 | Two key vendors (e.g. cloud hosting, AI model provider) |
| `nda/` | Non-Disclosure Agreements | 2 | |
| `sow/` | Statements of Work | 2 | Both reference one of the MSAs |
| `policy/` | Compliance framework & policy | 2 | SOC 2-aligned framework excerpt + OpsVault's security policy |
| `audit-report/` | Vendor SOC 2 audit reports | 2 | **Synthetic**, labeled as such; one covers a vendor named in an MSA |
| `questionnaire/` | Customer security questionnaires | 1-2 | For the outbound direction |

Link the docs together so cross-document questions work. Both SOWs reference one MSA, and at least
one audit report covers a vendor named in a contract. Plant realistic PII so S5 has something to catch.

## PII protection (three layers)
**Redact people, not companies.**
- **Personal data of any individual** (customer, employee, signatory, auditor, notice contact): names,
  signatures, emails, phone numbers, home addresses, government IDs.
- **Secrets and financial data:** bank account and routing numbers, payment card numbers, API keys,
  passwords.
- **Keep:** vendor, company, and contract-party names, business addresses, and contract terms, so
  metadata (S4) and questions like "the cloud vendor's MSA" still work.

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
Vendor names are placeholders until the documents are written.
- "What's the liability cap in the cloud hosting vendor's MSA?" (single contract, exact number)
- "Which SOWs fall under that MSA?" (metadata / cross-reference)
- "What does OpsVault's policy require for access reviews?" (internal policy)
- "Does the AI model provider's contract forbid training on OpsVault customer data?" (current AI risk)
- "The cloud vendor's MSA requires encryption at rest. Does their SOC 2 report confirm it, and does that
  meet OpsVault's policy?" (cross-document, the showcase question)
- "A customer asks: do you encrypt data at rest? Answer from our SOC 2 and policy." (outbound)
