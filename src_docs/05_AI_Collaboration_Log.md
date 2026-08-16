# AI Collaboration Log

This project was built in direct, iterative collaboration with Claude (via Claude Code). This log documents where and how AI was used, what it produced, and where human judgment directed or corrected the outcome — in the interest of transparency about the AI-assisted workflow itself, not just the AI-assisted product.

## 1. Initial Product Proposal

**Prompt direction:** develop the "Medication Adherence & Interaction Copilot" idea (one of four AI product ideas surfaced) into a full proposal covering opportunity assessment, segmentation, product strategy, UX, RICE prioritization, KPI framework, risk register, ethical impact note, roadmap, and monetization.

**AI produced:** the full `MedGuardian_AI_Product_Proposal.docx`, grounded in real, named, publicly-accessible data sources (DrugBank, RxNorm, openFDA) rather than hypothetical ones.

**Human direction:** selected this idea over three alternatives; approved the document structure and content.

## 2. MVP Prototype (Full-Vision Demo)

**Prompt direction:** "create a MVP in python with AI embedded into it," Sandoz blue color palette, AI must be present for both the client-facing experience and the team's own project-management artifacts.

**AI produced:** the Streamlit application (`app.py`, `ai_engine.py`, `mock_data.py`), including a dual-mode AI layer (live Claude API call with a deterministic rule-based fallback) so the app is demoable with or without an API key. Verified booting cleanly before delivery.

**Human direction:** specified the branding, the dual client/internal AI requirement, and reviewed the interpretation of "AI for project-management artifacts" when it was ambiguous.

## 3. Code Review & Positioning Decks

**Prompt direction:** requested a presentable slide summarizing reusability, target consumers, AI touchpoints, and AI value — then a second deck reframing the same product as evidence of a reusable AI *pattern* rather than a single feature.

**AI produced:** two decks (`MedGuardian_AI_Prototype_Review.pptx`, `MedGuardian_AI_Capabilities_Reuse.pptx`) after an actual code review of the existing app — findings were derived from reading the real source, not invented.

**Human direction:** approved scope and content of each deck.

## 4. Styling Bug Fix

**Prompt direction:** flagged that white text wasn't visible against light backgrounds — first in the deck, then clarified the report was actually about the running Streamlit app.

**AI produced:** diagnosed the actual cause via live computed-style inspection in-browser (Streamlit's dark-theme default was leaking through on unstyled elements), then fixed it with an explicit `.streamlit/config.toml` plus a defensive CSS override — verified the fix by re-inspecting computed styles, not just re-reading the code.

**Human direction:** caught the bug and corrected which artifact it applied to.

## 5. Product Overview Deck & Specialty Pharma Extension

**Prompt direction:** generate a full slide deck from the proposal docx; separately, asked a set of hard questions (what category is this product in vs. named competitors; how to pitch it in 3 minutes; what are PBMs) that led to identifying a gap — the proposal never named pharma manufacturers as a buyer, only PBMs/health plans.

**AI produced:** the 19-slide (later 21-slide) overview deck; a new Section 13 (Specialty Pharma Extension) added to the docx and deck, including an original closing-the-loop diagram (native vector shapes in the deck, a separately generated PNG for the docx) illustrating physician/patient/pharmacist/pharma data flow.

**Human direction:** asked the questions that surfaced the gap; did not specify the extension's content — that was AI-authored based on the identified gap, then reviewed and accepted.

## 6. Professor Pushback → Regulatory & Framing Additions

**Prompt direction:** relayed a professor's critique (the approval timeline is long; if I need to know a drug, I already know it and so does my physician) and separately shared a similar analysis from another AI session.

**AI produced:** an independent assessment (not assumed to agree with the pasted content — flagged one factual mischaracterization in it and one set of unverifiable figures) — this **independently converged on the same root-cause argument** (the fragmentation/visibility gap) given separately in an earlier turn, which was treated as a signal the reasoning was sound rather than accepted uncritically. Then implemented the agreed scope: a sharpened "Why isn't this already solved?" argument in Section 2.1 and Executive Summary, and a new Section 9.7 (Regulatory Positioning & Timeline) with an explicit non-SaMD target and a two-path timeline comparison — added to the docx and as two new slides in the deck.

**Human direction:** explicitly chose "targeted strengthening" over a full reposition when asked, since the underlying GTM strategy in the existing proposal was already correct.

## 7. Business Questions (Revenue, Deployment Readiness)

**Prompt direction:** asked whether the product should be deployed and what revenue it could realistically generate, before building MVP 1.

**AI produced:** a bottom-up, explicitly caveated illustrative revenue model (not a top-down TAM claim) mapped to the roadmap's own phase milestones, and a direct answer distinguishing "buildable as a startup" from "ready to deploy to real patients today" (the latter requires the security/compliance items already named in the risk register).

**Human direction:** asked the question; no correction needed to the framing given.

## 8. MVP 1 — First Build

**Prompt direction:** build a "defined MVP 1" with documentation and code, after confirming (via an explicit scope question) that MVP 1 should mean *strictly* the roadmap's own Phase 1 definition — not the full-vision demo's broader feature set.

**AI produced:** a new `mvp1/` folder, a single-file Streamlit app trimmed to exactly the RICE P0 items, plus `MVP1_Specification.docx`. Verified in-browser: real FDA drug search, correct interaction detection, correct pharmacist-queue routing.

**Human direction:** made the scope decision explicitly when asked; separately, had already independently pulled real FDA Orange Book data into the project (`orange_book_dataset_generator.py`, `data/`) — AI discovered this mid-task and used it in place of the earlier hand-picked drug list, rather than continuing with fabricated data.

## 9. MVP 1 — Restructure Against a Reference Example

**Prompt direction:** provided `SpendSightAI-main.zip`, a completed peer submission for the same course, and asked for the fuller deliverable structure it implied, then specifically asked to rebuild MVP 1 following its pattern.

**AI produced:** inspected the peer example's **structure only** (file layout, config pattern, test pattern) — explicitly did not read or reuse its actual business-logic content, which belongs to another student. Rebuilt MVP 1 into a config-driven, modular codebase (`src/` / `dashboards/` / `tests/`) with 25 new pytest tests covering the safety-critical interaction-detection and drug-normalization logic. Re-verified the full user flow in-browser after the refactor to confirm no regression.

**Human direction:** provided the reference file and set the sequencing ("finish MVP 1 first, then repackage everything") when asked to choose between three options.

## 10. This Documentation Set

**Prompt direction:** requested the `.md` files matching the peer example's `src_docs/` structure.

**AI produced:** this folder — built entirely from content already established across the docx, the deck, the code, and this conversation. No content was invented that hadn't already been decided or verified earlier in the project.

## Summary

Across the project, AI was used for: drafting structured business/strategy documents from stated requirements, generating and iterating application code, running and interpreting test suites, verifying UI behavior via live browser inspection rather than assumption, and synthesizing prior conversational context into new artifacts. Human judgment governed: which idea to pursue, which scope decisions to make at each fork (flagged explicitly via clarifying questions), what counted as a valid critique versus a mischaracterization, and final approval of every deliverable.
