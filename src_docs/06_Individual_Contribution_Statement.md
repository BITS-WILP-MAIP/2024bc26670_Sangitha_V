# Individual Contribution Statement

> **This file is a template, not a completed statement.** It cannot be filled in by AI — it's a personal/academic declaration of who on the team did what, and it needs to reflect your actual individual work and judgment, not a generated summary. Replace every `[ ]` placeholder below before submitting.

## Team & Roles

| Name | Role on this project | Primary sections/artifacts owned |
|---|---|---|
| Sangitha V | Sole Author | Full product proposal (13 sections, incl. Specialty Pharma Extension and Regulatory Positioning); MVP 1 codebase, tests, and docs; three presentation decks (prototype review, capabilities/reuse, full overview) plus the MVP 1 spec; `src_docs/` phase documentation and architecture diagram |

*(Individual submission — sole contributor.)*

## What I Personally Decided vs. What AI Drafted

Be specific — a reviewer wants to see judgment, not just output. Suggested structure, edit freely:

- **Content I directed but AI drafted:** All AI product control — direction, prompting, and review of the product proposal, MVP 1 codebase, presentation decks, and Phase 2 preview features — was done by myself.
- **Content I wrote or substantially edited myself:** All repository content (code, docs, decks) was AI-drafted under my direction and review; my own contribution took the form of direction, feature/bug diagnosis from actually using the running app (e.g. identifying the unreadable FDA interaction text, the missing per-drug check-in, the missing regimen view), and scoping decisions rather than hand-written prose or code.

## What I'd Do Differently

Before treating this as more than a demo scaffold, I'd validate the illustrative "regimen role" tags (first-line vs. add-on) and the 7-drug pairwise interaction table with an actual pharmacist — both are my own placeholder taxonomy, not sourced from a clinical reference. The pairwise interaction data still isn't a licensed source (DrugBank/FAERS); the openFDA label-text summarization I added is a real workaround for readability, not a substitute for that gap. The Phase 2 AI layer (summarization + chatbot) needs real output review before it could ever reach a patient — its only safety net right now is "recommend a pharmacist," which was a reasonable MVP-preview boundary but not sufficient for production. I'd also note that walling the chatbot off from the Phase 1 core was a decision I made reactively, after seeing the unreadable interaction text firsthand, rather than something planned from the start — the biggest open risk is that MVP 1's safety claims are only as strong as its zero-AI Phase 1 core, and the Phase 2 preview needs its own, separate validation before it earns the same trust.

Drawing on my experience with patient analytics, I believe this application could serve as a bridge for patients to track their medication regimen on a daily basis. Moreover, if the application succeeds in Phase 1, it could progress to Phase 2 and pursue classification as Software as a Medical Device (SaMD) — a regulatory approval process that could take around one to two years.

## Time Investment (Optional — check your course's rubric for whether this is required)

| Activity | Approximate time |
|---|---|
| Strategy & proposal development | About 24 hours, including time spent connecting with the marketing team to brainstorm before reviewing the existing code and product proposal, working through feature ideas like the auto-message/family-branching flow, and figuring out what was realistically doable for Phase 1 before committing to a build. |
| Prototype development & testing | About 40 hours — where most of the effort went, restructuring MVP 1 after studying a peer example's engineering pattern, pulling in real FDA data, and then iterating the dashboard multiple times based on actually using it (medication remove/reset, per-drug check-ins, the regimen view, and the AI summarization layer). |
| Documentation & presentation | About 15 hours, putting together several presentation decks, the full `src_docs` write-up, the architecture diagram, and this statement. |

---

*Signed:* Sangitha V, 2026-08-16
