# SafarGate — Application-Readiness Copilot

[![Hack-Nation 6](https://img.shields.io/badge/🏆_Hack--Nation_6-Challenge_03-blue?style=flat-square)](https://hack-nation.org/)
[![Status](https://img.shields.io/badge/Status-Active_Development-success?style=flat-square)]()
[![Tech Stack](https://img.shields.io/badge/TypeScript-59.5%25%20|%20React%20|%20Python%20API-blue?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)]()

> **An AI-powered companion that helps renters get ready to apply for affordable housing.** Transform scattered documents into a verified profile, understand program eligibility rules with real citations, and export a complete application packet—all while maintaining strict privacy and transparency.

---

## 🎯 The Problem We Solve

**Mohamed** is an international grad student moving to Boston. He's got:
- A partial assistantship (irregular income)
- Part-time campus work
- No local credit history
- Housing documents in multiple formats

He needs to apply for **LIHTC** affordable housing. But eligibility rules are opaque, documents are scattered, and one mistake can mean rejection.

**SafarGate** is his guide: extract → understand → prepare → apply.

---

## 🔒 Our Core Promise

**SafarGate never decides eligibility.** Period.

- ✅ **Extracts** document evidence with confidence scores & source citations
- ✅ **Explains** program rules with exact official citations
- ✅ **Calculates** income vs. thresholds deterministically
- ✅ **Prepares** a complete, exportable application packet

❌ **Never approves, denies, scores, or infers** eligibility  
❌ **Never uses hidden demographic proxies**  
❌ **Never trains on your data** — encrypted, ephemeral, fully deletable  

**The renter confirms every step. A qualified human decides.**

---

## 📋 Frozen Scope (Locked for the Event)

| Dimension | Scope |
|---|---|
| **Metro Area** | Boston-Cambridge-Quincy, MA-NH HUD Metro FMR Area |
| **Program** | LIHTC, FY2026 MTSP income limits (effective 2026-05-01) |
| **Data Source** | Real HUD data + organizer-provided synthetic documents |

> Depth beats breadth. We nail one flow perfectly instead of spreading across many.

---

## ✨ What Makes SafarGate Stand Out

### 1. **Three-Step Journey UI**
   - **Profile**: Upload documents → see extracted evidence with source highlights
   - **Understand**: Ask eligibility rules → get exact citations from the rule corpus
   - **Prepare**: Review checklist → export or delete your complete session

### 2. **Visible Confidence & Source**
   - No black-box confidence percentages
   - Every extracted field shows: **source document** + **page number** + **plain-language confidence** ("high", "needs review", "uncertain")
   - One-click correction that propagates downstream

### 3. **Citation-First Explanations**
   - Rules questions answered with exact official citations
   - Links back to the FY2026 MTSP rule corpus
   - Deterministic calculation with effective dates shown

### 4. **Built-In Trust & Safety**
   - In-app panel showing what's stored, encrypted, and deleted
   - Live demo of session deletion (data actually disappears)
   - Proof against prompt injection and adversarial input

### 5. **Accessibility-First Design**
   - WCAG 2.2 AA compliant
   - Full keyboard navigation
   - Visible focus indicators
   - No color-only status indicators
   - Labeled controls & clear error messages

---

## 🏗️ Repository Structure

```
SafarGate/
├── 📄 README.md                        ← You are here
├── 📂 docs/
│   ├── roadmap.md                      # Step-by-step build plan
│   ├── architecture.md                 # System diagram & explanation
│   └── risk_note.md                    # Security & architecture note
│
├── 📂 data/                            # FROZEN — Do not edit
│   ├── mtsp_2026_boston_cambridge_quincy.csv
│   ├── lihtc_boston_metro_subset.csv
│   ├── property_data_dictionary.csv
│   └── realdoor_data_pack.xlsx
│
├── 📂 rules/                           # FROZEN — Official rule corpus
│   ├── rule_corpus.jsonl
│   └── RULES_README.md
│
├── 📂 synthetic_documents/             # FROZEN — Test documents
│   ├── documents/                      # 24 synthetic PDFs (pay stubs, letters, etc.)
│   └── gold/                           # Gold standard answers + page coordinates
│
├── 📂 evaluation/                      # FROZEN — Pre-flight testing
│   ├── qa_gold.jsonl
│   ├── adversarial_tests.jsonl
│   └── application_checklists.json
│
├── 📂 governance/                      # FROZEN — Compliance docs
│   ├── DATA_USE_AND_SAFETY.md
│   └── LICENSE_MANIFEST.csv
│
├── 📂 backend/                         # 🔧 OUR BUILD — API & Logic
│   ├── app/
│   │   ├── main.py                     # FastAPI entrypoint
│   │   ├── extraction/                 # Document → allowlisted fields
│   │   ├── calculate.py                # Deterministic income calculator
│   │   ├── rules_engine.py             # Rule corpus + citation lookup
│   │   ├── packet/                     # Checklist diff + export
│   │   └── storage/                    # Session-scoped, encrypted storage
│   ├── tests/
│   └── requirements.txt
│
├── 📂 ai/                              # 🔧 OUR BUILD — Extraction & Explanation
│   ├── prompts/                        # Extraction & explanation templates
│   ├── extraction_pipeline.py          # OCR/parsing + confidence scoring
│   └── citation_engine.py              # Rule retrieval + citation formatting
│
├── 📂 security/                        # 🔧 OUR BUILD — Safeguards
│   ├── allowlist_filter.py             # Hard-enforced field allowlist
│   ├── injection_tests/                # Adversarial test cases
│   └── session_deletion_test.py        # Proves data deletion works
│
├── 📂 frontend/                        # 🔧 OUR BUILD — React UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProgressRail/           # 3-step indicator
│   │   │   ├── ProfileStep/            # Doc upload + source box + confidence
│   │   │   ├── UnderstandStep/         # Rules Q&A + citation + calculation
│   │   │   ├── PrepareStep/            # Checklist + preview + export/delete
│   │   │   └── TrustSafetyPanel/       # Storage transparency
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
│
└── 📂 scripts/
    └── run_tests.sh                    # Run all backend + starter tests
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **npm** or **yarn**

### Installation

#### 🖥️ **Windows**

```bash
# 1. Clone the repository
git clone https://github.com/Elve-ndev/SafarGate.git
cd SafarGate

# 2. Verify starter pack (optional but recommended)
cd data
python -m unittest discover -s tests -v
cd ..

# 3. Set up Python virtual environment
python -m venv venv
venv\Scripts\activate  # On PowerShell: venv\Scripts\Activate.ps1

# 4. Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# 5. Install frontend dependencies
cd frontend
npm install
cd ..

# 6. Start the backend API (from SafarGate root)
cd backend
python -m app.main

# 7. In a new terminal, start the frontend
cd frontend
npm run dev
```

**Frontend**: Open http://localhost:5173 (or as shown in terminal)  
**Backend API**: http://localhost:8000 (docs at /docs)

---

#### 🐧 **Linux / macOS**

```bash
# 1. Clone the repository
git clone https://github.com/Elve-ndev/SafarGate.git
cd SafarGate

# 2. Verify starter pack (optional but recommended)
cd data
python -m unittest discover -s tests -v
cd ..

# 3. Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# 5. Install frontend dependencies
cd frontend
npm install
cd ..

# 6. Start the backend API (from SafarGate root)
cd backend
python -m app.main &

# 7. Start the frontend
cd frontend
npm run dev
```

**Frontend**: Open http://localhost:5173 (or as shown in terminal)  
**Backend API**: http://localhost:8000 (docs at /docs)

---

## 📱 Application Screenshots

> **Add application demo screenshots here:**

```
[Screenshots showing:]
1. Profile Step — Document upload with extracted evidence
2. Understand Step — Rules question with citation
3. Prepare Step — Checklist preview & export
4. Trust & Safety Panel — Session transparency
```

---

## 🎬 Required Demo Flow

This is what judges will test live:

1. **📤 Upload a Document**
   - Show extracted evidence with source highlights & confidence levels

2. **✏️ Correct a Field**
   - Change an extracted value & show how it propagates to the calculation

3. **❓ Ask a Rules Question**
   - "Can I qualify if my income is $45,000?" → Show exact MTSP citation

4. **🧮 Show the Calculation**
   - Display deterministic income vs. threshold math with effective dates

5. **🚨 Flag Missing Documents**
   - Show checklist diff & export the incomplete packet

6. **🔒 Run Live Security Tests**
   - **Refusal Test**: Submit an injection prompt → system ignores it
   - **Prompt Injection Test**: Try to alter rules via document text → blocked
   - **Session Deletion Test**: Delete session → prove data is gone

---

## 👥 Team Roles & Ownership

| Role | Owns | Responsibilities |
|---|---|---|
| **AI** | `ai/` | Extraction confidence scoring, citation retrieval, plain-language explanations |
| **Backend** | `backend/` | Deterministic calculator, session storage, encryption, deletion, packet export |
| **Security** | `security/` | Allowlist enforcement, adversarial testing, live demo tests |
| **Frontend** | `frontend/` | 3-step journey UI, accessibility compliance, Trust & Safety transparency |

---

## 🛡️ Non-Negotiable Rules

These are **hard requirements** from the challenge brief:

- **❌ No decisioning** — We never approve, deny, score, rank, or state eligibility
- **❌ No hidden proxies** — We never infer demographic/protected traits; every feature is published
- **✅ Consent & correction** — Every extracted value is shown with source and can be corrected
- **🔐 Privacy & security** — Synthetic documents only, encrypted storage, ephemeral by default, full deletion, no training
- **⚠️ Untrusted input** — Document text is never trusted; embedded prompts cannot alter behavior
- **♿ Accessible** — WCAG 2.2 AA: keyboard, focus, labeled controls, no color-only status

---

## 📊 Technical Stack

| Layer | Technology |
|---|---|
| **Frontend** | React + TypeScript + TanStack Start |
| **Backend** | Python 3.10+ + FastAPI |
| **Extraction** | OCR + LLM-based field extraction with confidence scoring |
| **Rules Engine** | Deterministic rule corpus lookup + citation formatter |
| **Storage** | Encrypted session storage with automatic expiry |
| **Testing** | Pytest, unittest, adversarial test suite |

---

## 🧪 Testing

```bash
# Run all backend tests
cd backend && python -m pytest tests/ -v

# Run security adversarial tests
cd security && python injection_tests.py && python session_deletion_test.py

# Run starter pack verification
cd data && python -m unittest discover -s tests -v
```

---

## 📖 Documentation

- **[docs/roadmap.md](docs/roadmap.md)** — Step-by-step build plan
- **[docs/architecture.md](docs/architecture.md)** — System diagram & design decisions
- **[docs/risk_note.md](docs/risk_note.md)** — Security & fairness risk assessment
- **[governance/DATA_USE_AND_SAFETY.md](governance/DATA_USE_AND_SAFETY.md)** — Data handling policy
- **[rules/RULES_README.md](rules/RULES_README.md)** — Rule corpus format & citation guide

---

## ⚖️ License

SafarGate is built for **Hack-Nation 6** (Challenge 03, powered by RealPage).  
See [governance/LICENSE_MANIFEST.csv](governance/LICENSE_MANIFEST.csv) for full attribution.

---

## 🤝 Contributing

This repo is locked to the hackathon event scope. All changes should:
- Maintain the 3-step user journey
- Follow non-negotiable rules (above)
- Preserve frozen data, rules, & evaluation sets
- Include tests before pushing

---

## 💬 Questions?

Check the docs first — especially [docs/architecture.md](docs/architecture.md) and [governance/DATA_USE_AND_SAFETY.md](governance/DATA_USE_AND_SAFETY.md).

For **demo-specific issues**, see the **Required Demo Flow** section above.

---

<div align="center">

**Built with ❤️ for renters who deserve clarity and respect.**

*Making affordable housing applications fair, transparent, and human-centered.*

</div>
