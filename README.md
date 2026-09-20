# TRUTHCHAIN

> **"Don't just answer a claim. Investigate it."**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.2.35-black.svg)](https://nextjs.org/)
[![Groq LLM](https://img.shields.io/badge/LLM-Groq%20Cloud-f34f29.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TRUTHCHAIN** is an **Autonomous Agentic Evidence Investigation System**. Unlike generic search engines, document summarizers, or basic RAG chatbots, TRUTHCHAIN decomposes complex real-world claims into verifiable propositions, ingests heterogeneous evidence documents, executes deterministic mathematical and temporal verification, resolves cross-source contradictions, and generates auditable proof lineage with interactive graph visualizers.

---

## 💥 The Problem Statement: The Modern Information Integrity Crisis

In an era dominated by generative AI content, corporate spin, complex procurement fraud, and rapid misinformation spread, traditional factual verification tools fail due to four critical vulnerabilities:

1. **The RAG & LLM Hallucination Trap**: Generic RAG chatbots rely on probabilistic next-token generation. When asked whether a delivery of $10,000$ items met a deadline, LLMs frequently perform flawed mental arithmetic or accept plausible-sounding document summaries as fact without auditing source line items.
2. **Keyword & Vector Blindness**: Keyword search and semantic embeddings fail when evidence is split across mismatched formats—such as a PDF Purchase Order, an Excel Shipping Ledger, a DOCX Contract Clause, and a scanned Bill of Lading. Mismatched dates or split shipments escape standard similarity searches.
3. **The Single-Source Bias**: Traditional AI answers claims based on individual documents in isolation, completely missing cross-document discrepancies (e.g., Invoice says September 14, but Customs Gate Log proves physical arrival on September 17).
4. **Lack of Verifiable Audit Lineage**: Regulators, auditors, legal counsel, and investigative journalists cannot accept black-box AI answers. Every conclusion requires a mathematical and document-backed proof trace showing exact page spans, dates, and calculations.

### **The TRUTHCHAIN Paradigm Shift**
TRUTHCHAIN bridges the gap between **Generative Semantic Intelligence** and **Deterministic Mathematical Rigor**. It never simply "answers" a claim—it initiates a formal forensic investigation cycle.

---

## 🏗️ System Architecture & Investigation Lifecycle

```text
               +-------------------------------------------------------+
               |                  USER CLAIM STATEMENT                 |
               +-------------------------------------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |           CLAIM DECOMPOSITION ENGINE                  |
               |       (Groq LLM + Pydantic Proposition Schema)       |
               +-------------------------------------------------------+
                                           |
             +-----------------------------+-----------------------------+
             |                                                           |
             v                                                           v
+--------------------------+                               +--------------------------+
| MULTIMODAL INGESTION     |                               |  EXTERNAL SEARCH ENGINE  |
|  - RapidOCR Engine       |                               |   - Tavily API           |
|  - PDF, DOCX, XLSX, PNG  |                               |   - DuckDuckGo REST      |
+--------------------------+                               +--------------------------+
             |                                                           |
             +-----------------------------+-----------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |          EXTRACTED FACT & ENTITY RESOLUTION           |
               +-------------------------------------------------------+
                                           |
             +-----------------------------+-----------------------------+
             |                                                           |
             v                                                           v
+--------------------------+                               +--------------------------+
| DETERMINISTIC NUMERICAL  |                               | DETERMINISTIC TEMPORAL   |
|   (SymPy Math Engine)    |                               |   (Dateutil ISO Engine)  |
+--------------------------+                               +--------------------------+
             |                                                           |
             +-----------------------------+-----------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |           CONTRADICTION & DISCREPANCY ENGINE          |
               |        (Cross-Source Conflict & Hypothesis Grid)      |
               +-------------------------------------------------------+
                                           |
             +-----------------------------+-----------------------------+
             |                                                           |
             v                                                           v
+--------------------------+                               +--------------------------+
| ADVERSARIAL RED-TEAM     |                               | INTERACTIVE PROOF GRAPH  |
|   (Falsification Mode)   |                               |   (React Flow Visualizer)|
+--------------------------+                               +--------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |         PDF REPORT & PROOF TRACE GENERATION           |
               +-------------------------------------------------------+
```

---

## ⚡ Core Subsystems & Technical Features

### 1. 🧬 Claim Decomposition Engine (`ClaimEngine`)
- **Dynamic Semantic Splitting**: Breaks arbitrary claims across any domain into atomic subclaims (Entity & Contract propositions, Quantity/Specification propositions, Temporal/Deadline propositions).
- **Pydantic Validation**: Guarantees typed outputs for subject, predicate, object, constraints, and verification requirements.

### 2. 📄 Multimodal Document & OCR Ingestion (`IngestionEngine` & `OCRService`)
- **Deployment-Safe OCR**: Integrates **RapidOCR** (Pure Python ONNX runtime wheel) to process PNG, JPG, WEBP images, and scanned image-only PDF pages without system binary dependencies.
- **Heterogeneous Format Support**: Native parsing for PDF text layers, DOCX word documents, CSV/XLSX spreadsheets, and JSON records.

### 3. 🌐 Real External Web Evidence Search (`ExternalSearchService`)
- **Query Synthesis**: Automatically constructs targeted web queries from identified evidence gaps.
- **Dual-Engine Execution**: Queries Tavily Search API when configured, with seamless fallback to zero-cost DuckDuckGo REST search.
- **SSRF & Security Shield**: Validates hostnames to block private/internal IP ranges (`127.0.0.1`, `10.x`, `192.168.x`, `169.254.169.254`) and sanitizes external HTML against prompt injection attacks.

### 4. 🔢 Deterministic Verification Engines (`NumericalEngine` & `TemporalEngine`)
- **Mathematical Accuracy**: Performs strict quantity reconciliation ($8,500 + 1,500 = 10,000$) using Python native math and SymPy, preventing LLM arithmetic errors.
- **Temporal Alignment**: Normalizes ambiguous dates ("Sept 15", "2026-09-15", "15/09/2026") to ISO-8601 format and evaluates deadline compliance deterministically.

### 5. ⚔️ Contradiction & Adversarial Red-Team Engine (`ContradictionEngine`)
- **Conflict Identification**: Automatically compares extracted facts from different sources to flag delivery date mismatches, quantity shortfalls, or missing authorizations.
- **Red-Team Falsification Mode**: Actively attempts to disprove claims by prioritizing search for penalty defaults, late waivers, or unfulfilled contract clauses.

### 6. 🌐 Interactive Evidence Graph & PDF Export (`GraphEngine` & `ReportEngine`)
- **React Flow Visualizer**: Renders interactive graph networks linking claims, sources, facts, contradictions, and evidence gaps.
- **ReportLab PDF Generation**: Produces publication-grade PDF investigation reports complete with metadata, line-item provenance, and verdict reasoning.

---

## 🔌 Comprehensive API Reference

### Health & System Status
- `GET /health`: Returns system health, database connection state, and deployment environment.

### Investigation & Case Operations
- `GET /api/cases`: Lists all active and historical investigation cases.
- `POST /api/cases`: Creates a new case and automatically triggers claim decomposition.
- `GET /api/cases/{id}`: Returns complete case state including atomic claims, ingested sources, events, contradictions, hypotheses, evidence gaps, and audit steps.
- `POST /api/cases/{id}/search`: Triggers real external web search to discover and ingest web evidence for missing gaps.
- `GET /api/cases/{id}/graph`: Generates React Flow node/edge graph payload representing evidence relationships.
- `POST /api/cases/{id}/challenge`: Re-opens investigation under a user challenge question or counter-hypothesis.
- `POST /api/cases/{id}/red-team`: Activates adversarial falsification mode ("Try to disprove this claim").
- `GET /api/cases/{id}/report`: Generates and streams downloadable PDF investigation report.
- `POST /api/demo/load`: Instantly loads the 11-file medical procurement demonstration case.

---

## 🛠️ Local Installation & Setup Guide

### Prerequisites
- Python 3.10 or higher
- Node.js v18 or higher
- Git

### 1. Clone Repository
```bash
git clone https://github.com/SatAi999/TruthChain.git
cd TruthChain
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Configure environment variables
cp .env.example .env
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

### 4. Running the Application
```bash
# Terminal 1: Start Backend API (Port 8000)
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Start Frontend Dev Server (Port 3005)
cd frontend
npm run dev -- -p 3005
```

Open [http://localhost:3005](http://localhost:3005) in your web browser.

---

## 🧪 Quality Assurance & Test Verification

TRUTHCHAIN includes a comprehensive automated test suite guaranteeing **zero-mock runtime execution**:

```bash
# Execute Backend Pytest Suite
PYTHONPATH=backend pytest backend/tests/
```

**Results**: `23/23 Passed (100% Success Rate)`

```bash
# Execute Frontend Next.js Production Build
npm --prefix frontend run build
```

**Results**: `0 Errors (Compiled successfully across all 7 routes)`

---

## 🌐 Production Deployment Blueprint

TRUTHCHAIN is pre-configured for seamless production deployment:

- **Backend Web Service**: Deployable to **Render** using Python runtime (`uvicorn main:app --host 0.0.0.0 --port $PORT`).
- **Database**: Configured for **PostgreSQL** in production with SQLite development fallback (`DATABASE_URL`).
- **Frontend App**: Deployable to **Vercel** with Next.js framework preset (`NEXT_PUBLIC_API_URL`).

Refer to [DEPLOYMENT.md](file:///d:/HackDay/DEPLOYMENT.md) for full deployment parameters.

---

## 🌍 Transformative Real-World Applications

TRUTHCHAIN's agentic evidence intelligence model unlocks high-impact enterprise and public sector applications:

### 1. 🏥 Government & Corporate Procurement Audit
- **Challenge**: Multimillion-dollar medical device or infrastructure contracts with thousands of line-item invoices, shipping manifests, and gate passes.
- **TRUTHCHAIN Impact**: Automatically verifies whether claimed quantities reached destination hospitals before contractual deadlines, flagging partial deliveries, unapproved waivers, or invoice inflation.

### 2. ⚖️ Legal Discovery & Litigation Support
- **Challenge**: Sifting through 100,000+ discovery records to find timeline contradictions between witness depositions and physical records.
- **TRUTHCHAIN Impact**: Builds unified chronological evidence graphs and highlights exact statement-versus-fact contradictions with source citations.

### 3. 🔍 Investigative Journalism & Fact-Checking
- **Challenge**: Rapidly fact-checking complex political claims regarding budget expenditures or policy outcomes backed by mixed whitepapers and speeches.
- **TRUTHCHAIN Impact**: Replaces surface-level text search with multi-document fact extraction, temporal checking, and adversarial red-teaming.

### 4. 🛡️ Insurance Fraud & Risk Assessment
- **Challenge**: Evaluating complex commercial property or cargo loss claims with conflicting damage reports and police logs.
- **TRUTHCHAIN Impact**: Performs cross-source entity resolution, timeline verification, and gap analysis to spot fraudulent or exaggerated claims.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
