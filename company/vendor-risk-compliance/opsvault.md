# Company: OpsVault (fictional)

**OpsVault is a fictional company** created for this portfolio project. It's modeled on
cloud enterprise workflow platforms: one platform that runs a company's IT, HR, customer service,
risk, finance, and supply-chain workflows, with AI agents built in. It isn't affiliated with or based
on any real company's internal documents. Every OpsVault policy, contract, and audit report in `data/` is synthetic.

## Overview
OpsVault is a SaaS company that sells workflow automation and AI on its own platform. Customers buy
ready-made products (SaaS) or build their own apps on the OpsVault Platform (PaaS).

**Customer Zero:** OpsVault runs every product internally first, then sells what worked. This RAG
system follows the same path: OpsVault's own teams use it first, then it ships to customers.

## Products

| Product | What it does |
|---|---|
| OpsVault Platform | Low-code platform, workflow engine, database, APIs (incl. a Table API) |
| OpsVault AI | Generative AI assistants and AI agents built into every product |
| OpsVault IT Service | Incidents, changes, and service requests |
| OpsVault IT Operations | Asset inventory (CMDB), monitoring, AIOps |
| OpsVault Security Ops | Security incidents and vulnerability response |
| OpsVault Risk & Compliance | Policies, audits, and **vendor risk** (this system's home) |
| OpsVault HR Service | Employee requests and onboarding |
| OpsVault Customer Service | Customer cases and field service |
| OpsVault App Builder | Customers build their own apps |
| OpsVault Finance Ops | Invoices, accounts payable, month-end close, spend approvals |
| OpsVault Supply Chain | Supplier onboarding, purchase orders, source-to-pay (this system's second home) |
| OpsVault CRM | Sales, quotes, orders, customer accounts |
| OpsVault ERP Connect | Two-way sync with SAP, Oracle, and NetSuite without copying data |

## Key vendors
| Vendor type | Why it matters | Showcase clause |
|---|---|---|
| Cloud hosting provider | Runs the OpsVault Platform | Encryption at rest |
| AI model provider | Powers OpsVault AI | No training on customer data |
| Payments / ERP provider (optional) | Touches financial data | SOX and PCI controls |
| Logistics / supplier network (optional) | Supply chain | Right to audit |

## Compliance
- **SOC 2 Type II**, the primary framework (control IDs like `CC6.1`, `CC7.2`, `CC8.1`).
- **SOX** for finance-related vendors and controls.
- **PCI DSS** wherever payment card data is involved.

## Who uses the RAG system
Procurement, security, GRC (governance, risk & compliance), legal, and sales (for customer security
questionnaires).
