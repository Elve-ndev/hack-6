# hack-6[README.md](https://github.com/user-attachments/files/30156733/README.md)
# RealDoor — Application-Readiness Copilot
### Hack-Nation 6th Global AI Hackathon · Challenge 03 · Powered by RealPage

An AI copilot that helps a renter get **ready** to apply for affordable housing — turning their documents into a confirmed profile, explaining one program's rules with citations, flagging missing paperwork, and preparing a packet they fully control.

**RealDoor never decides eligibility. It extracts, explains, calculates, and prepares. The renter confirms. A qualified human decides.**

---

## The story

**Mohamed** is an international grad student (Morocco/Pakistan background) moving to the Boston-Cambridge-Quincy area to study. He's on a partial assistantship, works part-time on campus, and has never navigated the US affordable-housing system before. He doesn't know what LIHTC is, what documents count as proof of income, or what "MTSP limits" means. RealDoor walks him through getting application-ready — without ever telling him "yes, you qualify."

## Frozen scope (do not change)

| | |
|---|---|
| **Metro** | Boston-Cambridge-Quincy, MA-NH HUD Metro FMR Area |
| **Program** | LIHTC, FY2026 MTSP income limits (effective 2026-05-01) |
| **Data source** | Organizer-provided starter pack (real HUD data, synthetic test documents) |

This scope is locked for the whole event. Depth and correctness on one flow beats breadth across many.

## Non-negotiable rules (from the challenge brief)

- **No decisioning** — never approve, deny, score, rank, or state eligibility.
- **No hidden proxies** — no inferred demographic/protected traits; every feature we use is published.
- **Consent & correction** — every extracted value is shown with its source and can be corrected.
- **Privacy & security** — synthetic documents only, encrypted storage, ephemeral by default, full session deletion, no training on uploads.
- **Untrusted input** — document text is never trusted; embedded instructions must never change system behavior.
- **Accessible** — WCAG 2.2 AA: full keyboard operation, visible focus, labeled controls/errors, no color-only status.

## Required demo flow

1. Upload a document → show extracted evidence (source + confidence).
2. Correct a field → show it propagates downstream.
3. Ask a rules question → show the exact citation.
4. Show the deterministic calculation + its effective date.
5. Flag a missing/expired document → export the packet.
6. Run the refusal test, the prompt-injection test, and the session-deletion test — live.

---

## Repository structure

```
realdoor-mohamed/
├── README.md                          # this file
├── docs/
│   ├── roadmap.md                     # step-by-step build plan
│   ├── architecture.md                # 1-page system diagram + explanation
│   └── risk_note.md                   # required risk/architecture note
│
├── data/                              # FROZEN — from organizer starter pack, do not edit
│   ├── mtsp_2026_boston_cambridge_quincy.csv
│   ├── lihtc_boston_metro_subset.csv
│   ├── property_data_dictionary.csv
│   └── realdoor_data_pack.xlsx
│
├── rules/                             # FROZEN — official rule corpus
│   ├── rule_corpus.jsonl
│   └── RULES_README.md
│
├── synthetic_documents/               # FROZEN — test documents + answer key
│   ├── documents/                     # 24 fake PDFs (pay stubs, letters, etc.)
│   └── gold/                          # correct extracted values + page coordinates
│
├── evaluation/                        # FROZEN — use to test yourselves before judges do
│   ├── qa_gold.jsonl
│   ├── adversarial_tests.jsonl
│   └── application_checklists.json
│
├── governance/                        # FROZEN — read once, follow always
│   ├── DATA_USE_AND_SAFETY.md
│   └── LICENSE_MANIFEST.csv
│
├── backend/                           # YOUR BUILD
│   ├── app/
│   │   ├── main.py                    # API entrypoint
│   │   ├── extraction/                # document → allowlisted fields
│   │   ├── calculate.py               # deterministic income vs. threshold math
│   │   ├── rules_engine.py            # loads rule corpus, finds relevant rule
│   │   ├── packet/                    # checklist diff + export generation
│   │   └── storage/                   # ephemeral/session-scoped, encrypted
│   ├── tests/
│   └── requirements.txt
│
├── ai/                                # YOUR BUILD
│   ├── prompts/                       # extraction + explanation prompts
│   ├── extraction_pipeline.py         # OCR/parsing + confidence scoring
│   └── citation_engine.py             # retrieval + citation formatting
│
├── security/                          # YOUR BUILD
│   ├── allowlist_filter.py            # hard-enforced field allowlist
│   ├── injection_tests/               # prompt-injection test cases
│   └── session_deletion_test.py       # proves data is actually gone
│
├── frontend/                          # YOUR BUILD
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProgressRail/          # Profile → Understand → Prepare
│   │   │   ├── ProfileStep/           # doc upload + source box + confidence
│   │   │   ├── UnderstandStep/        # rules Q&A + citation + calculation
│   │   │   ├── PrepareStep/           # checklist + preview + export/delete
│   │   │   └── TrustSafetyPanel/      # what's stored/encrypted/deleted
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
│
└── scripts/
    └── run_tests.sh                   # runs backend + starter pack tests
```

## Quick start

```bash
# 1. Verify the starter pack works
cd data/../starter && python -m unittest discover -s tests -v

# 2. Install backend deps
cd backend && pip install -r requirements.txt

# 3. Install frontend deps
cd frontend && npm install
```

## Team roles

| Role | Owns |
|---|---|
| **AI** | `ai/`, extraction confidence, citation logic, plain-language explanations |
| **Backend** | `backend/`, deterministic calculator, storage/encryption/deletion, packet export |
| **Security** | `security/`, allowlist enforcement, adversarial tests, live demo tests 6a-6c |
| **Frontend** | `frontend/`, 3-step journey UI, accessibility, Trust & Safety panel |

## What makes this submission stand out
1. Visible progress rail across the 3 stages.
2. Plain-language confidence labels, not raw percentages.
3. In-app Trust & Safety panel.
4. Micro-explainers per checklist item, written for a first-time international renter.
5. Abstention responses that guide the user to the fix, not a dead end.
