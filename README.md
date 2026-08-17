<img src="medguardian_logo_full.png" alt="MedGuardian AI logo" width="360">

# MedGuardian AI — Final Submission

**Management of AI Products (MBACC ZG583) — Capstone**
**Sangitha V — Sole Author**

An AI-powered medication adherence and drug-interaction copilot for patients managing multiple
chronic prescriptions. This repo is the final submission package — the reasoning behind every
decision here is in `02_Final_Report.pdf`.

## What's in this repo

| File / Folder | What it is |
|---|---|
| `01_Executive_Summary.pdf` | Problem, target user, product concept, why AI, recommendation — 2 pages |
| `02_Final_Report.pdf` | Product strategy, PM artifact pack, UX/trust design, data/model/evaluation strategy, business/economics/scaling, ethics/governance/risk |
| `03_Presentation_Deck.pdf` | 10-slide final review deck |
| `04_Prototype_Readme_or_Link.md` | Pointer to the prototype and how to run it |
| `05_AI_Collaboration_Log.md` | Honest account of where AI helped, where it was wrong, and what was corrected |
| `06_Individual_Contribution_Statement.pdf` | Signed individual contribution statement |
| `MVP1/` | The working prototype — see below |
| `Appendix/` | PRD, wireframes, metrics framework, roadmap, risk note, architecture diagram, and screenshots of the running app |

## Running the prototype

```bash
cd MVP1
pip install -r requirements.txt
streamlit run dashboards/app.py
```

Three pages ship with zero AI/LLM dependency — Patient Dashboard's interaction checks, Pharmacist
Review Queue, KPI Dashboard. A separate, clearly-labeled Phase 2 Preview page opts into a live
Claude integration (FDA-label summarization + a medication Q&A chatbot); see `MVP1/.env.example`
if you want to try that part with your own API key. Neither is required to run or test the core.

## Running the tests

```bash
cd MVP1
pytest tests/ -v
```

47 tests, all passing — covering the interaction engine, drug normalization, adherence tracking,
FDA reference parsing, session-state handling, and the AI layer's deterministic fallback paths.

## Scope note

This is a strictly-scoped Phase 1 build (see `Appendix/Roadmap/Product_Roadmap.md`) — a single
condition, one language, and an illustrative reference dataset. It is not built or validated for
real clinical use; `Appendix/Risk_Note/Risk_Note.md` and Section 6 of `02_Final_Report.pdf` cover
what would need to change before that.
