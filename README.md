# SafarGate — Application-Readiness Copilot

[![Hack-Nation 6](https://img.shields.io/badge/🏆_Hack--Nation_6-Challenge_03-blue?style=flat-square)](https://hack-nation.org/)
[![Status](https://img.shields.io/badge/Status-Active_Development-success?style=flat-square)]()
[![Tech Stack](https://img.shields.io/badge/TypeScript-59.5%25%20|%20React%20|%20Python%20API-blue?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)]()

> **An AI-powered companion that helps renters—especially students in need—get ready to apply for affordable housing.** Transform scattered documents into a verified profile, understand program eligibility rules with real citations, and export a complete, human-reviewed application packet.

---

## 🎯 The Problem We Solve

**Mohamed** is an international grad student moving to Boston. He's got:
- A partial assistantship (irregular income)
- Part-time campus work
- No local credit history
- Housing documents in multiple formats
- **Language barriers and unfamiliar U.S. housing systems**

He needs to apply for **LIHTC** affordable housing. But eligibility rules are opaque, documents are scattered, and one mistake can mean rejection—especially for students navigating a new country's bureaucracy.

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

### 🎯 **1. Built for Students and Low-Income Renters—Not Just General Users**

SafarGate specifically addresses the challenges **international and domestic students face** when applying for affordable housing:

- **Irregular, multiple income sources** (assistantships, part-time work, grants) — parsed correctly without requiring a single "primary employer"
- **Language-forward design** — clear error messages, no jargon, step-by-step guidance written for first-time international renters
- **No credit score bias** — focuses only on income verification, not credit history
- **Document flexibility** — accepts synthetic documents that mimic real student life (benefit letters, assistantship verification, campus employment stubs)
- **Accessible to students without tech literacy** — full keyboard navigation, plain text, no complex UI patterns

This isn't "a tool that happens to help students." This is **designed from day one for students in need.**

---

### 💼 **2. Radical Transparency — Every Field Has a Source**

Every extracted piece of data shows:
- **Where it came from** (document name + page number)
- **Confidence level** (high / needs review / uncertain) — *no black-box percentages*
- **One-click correction** that cascades through income calculation and checklist

This is **not standard.** Most extraction tools hide confidence scores or don't link back to source documents. We make corrections visible and immediate—critical for students reviewing their own documents in unfamiliar systems.

---

### 🔗 **3. Citation-First Rule Explanations — No Guessing**

Students ask: *"Can I qualify with $45,000 income?"*

Instead of an AI guess, they get:
- The exact **HUD rule text** from the official FY2026 MTSP corpus
- Direct link to the **source document** with locator
- **Effective date** showing when the rule applies
- **Deterministic math:** income vs. threshold, plainly stated

This prevents the most dangerous failure mode: a student believes they're ineligible based on an AI hallucination—or worse, doesn't apply at all because the system confused them.

---

### 🛡️ **4. Trust & Safety Built Into the UI, Not Hidden**

- **In-app session panel** showing what's stored, what's encrypted, what's deleted
- **Live demo of session deletion** — watch your data actually disappear (critical for international students concerned about data privacy)
- **Adversarial proof** against prompt injection and hidden instructions in documents
- **WCAG 2.2 AA** accessibility — designed for people with disabilities, low tech literacy, and non-English backgrounds

Most AI tools hide their safeguards. We make them visible and testable by judges—and by students who need proof their data is safe.

---

### 🧮 **5. Deterministic Income Calculation — No AI Randomness**

The annualized income calculation is **separated from AI** and runs in pure Python:
- Handles multiple income sources (assistantship + part-time work + research grants)
- Correctly interprets pay periods (weekly, bi-weekly, monthly, annual)
- Parses date ranges to infer pay frequency from documents
- **Reproducible:** same input → same output, always

No neural network doing income math. No hallucinations. No weekend vs. weekday bias. This is especially important for students with irregular income streams.

---

### 🎨 **6. Three-Step Journey Designed for Real Renter & Student Workflows**

- **Profile** → Upload docs, see extracted fields with source highlights, correct as needed
- **Understand** → Ask rules questions, get official citations, understand the threshold
- **Prepare** → Review checklist, export complete packet for submission or deletion

The flow mirrors the *actual student workflow:* gather documents → understand the rules → prepare the packet. Not generic; specific to affordable housing and student life.

---

### ♿ **7. Accessibility as a Core Feature, Not an Afterthought**

- Full keyboard navigation (no mouse required)
- Visible focus indicators on every interactive element
- No color-only status indicators (red/green icons have text labels)
- Clear, tested error messages for international users
- Screen reader compatible with ARIA labels
- **Plain language** without housing-industry jargon

This isn't "we're accessible too." This is "accessibility is non-negotiable because our users—especially international students and those with disabilities—are often the most vulnerable renters."

---

### 🚫 **8. Hard Refusal to Decide Eligibility**

We **actively refuse** to:
- State whether a user "qualifies" or is "eligible"
- Rank applicants or score profiles
- Approve or deny based on any signal (even demographic proxies we might accidentally encode)
- Infer protected characteristics (race, national origin, disability, etc.)

If a student asks *"Will I get approved?"* we respond: *"That's a human decision. Here's your comparison [income vs. threshold]. A qualified reviewer will make the final call."*

This is a **trust boundary.** We cross it, we lose renters—and we fail our mission to support students fairly.

---

### 📊 **9. Real Data + Synthetic Test Suite Built for Student Scenarios**

- **Real HUD FY2026 MTSP income limits** for Boston-Cambridge-Quincy
- **24 synthetic test documents** including student-specific scenarios (assistantship letters, part-time employment stubs, research fellowship docs)
- **Gold standard answer key** with exact extracted values and page coordinates
- **Pre-baked adversarial tests** (prompt injection, hidden instructions, edge cases common in student documents)

Judges can test extraction accuracy and security rigor *before* they see the demo.

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


---

## 📱 Application Screenshots




![Profile Step](https://github.com/user-attachments/assets/ef5178da-9555-4b08-a7e5-dd68057a2a0f)

![Understand Step](https://github.com/user-attachments/assets/7ec81337-fd18-4b4a-8009-4444b5372aa4)

![Prepare Step](https://github.com/user-attachments/assets/7c3706b0-1f05-4f28-80ca-c006671e2b61)



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

**Built with ❤️ for students and renters who deserve clarity and respect.**

*Making affordable housing applications fair, transparent, and human-centered.*

</div>
