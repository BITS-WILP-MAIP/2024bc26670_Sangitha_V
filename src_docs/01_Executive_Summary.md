# Executive Summary

**Project:** MedGuardian AI
**Course:** Management of AI Products (MBACC ZG583)

## What it is

MedGuardian AI is an AI-powered medication adherence and drug-interaction copilot for patients managing multiple chronic-disease prescriptions ("polypharmacy"). It combines a rules-grounded interaction engine, built on open pharmacological data, with a generative-AI explanation layer, delivered as a mobile companion app that can also be embedded as a feature inside an existing pharmacy, health-insurer, or hospital app.

## The problem

Missed doses and unrecognized drug-drug interactions are a leading, preventable cause of hospital readmission among patients on three or more chronic medications. The gap isn't a knowledge gap in medicine — it's a **visibility gap**: a prescribing physician and a dispensing pharmacist each check interactions against the medication list they know about, at a single moment. Neither has continuous visibility into what a patient adds afterward — an over-the-counter painkiller, a supplement, a second prescription from a different specialist on a different record system.

## The design principle

MedGuardian addresses this with daily adherence nudges, plain-language interaction alerts, and a human-pharmacist escalation path for high-risk cases — an explicit **human-in-the-loop MVP design** rather than full automation from day one. The AI never has the final say on anything risky; every moderate- or high-risk output is held for a licensed pharmacist to approve or dismiss before it reaches the patient.

## What's been built

| Deliverable | What it covers |
|---|---|
| Product Proposal (`MedGuardian_AI_Product_Proposal.docx`) | Full opportunity assessment, segmentation, product strategy, UX, RICE prioritization, KPI framework, data sources, risk register, ethical impact note, roadmap, monetization, and the Specialty Pharma Extension |
| MVP 1 Specification (`MVP1_Specification.docx`) | The strictly-scoped Phase 1 build — exactly what would ship first |
| MVP 1 prototype (`mvp1/`) | A runnable, tested Streamlit application — zero AI/LLM dependency, real FDA drug data, 25 passing tests |
| Full-vision demo (`app.py`) | The complete product vision including the GenAI copilot, Physician View, and Pharma Program Insights |
| Presentation decks (3× `.pptx`) | Code/architecture review, AI capability positioning, and the full product overview as slides |

## Why this is buildable, not hypothetical

The proposal's opportunity assessment (Section 2.2) places MedGuardian in the **High Value / High Feasibility** quadrant: the core interaction logic runs on existing open pharmacological data (DrugBank, RxNorm, openFDA) without training a novel model, and the MVP's regulatory posture is deliberately non-SaMD — a decision-support tool with mandatory human review, not an autonomous diagnostic device — keeping time-to-pilot to roughly 3–6 months rather than the 12+ months a clinical-decision-support classification would require.

## Where the AI actually is

Two jobs, not one monolithic model: a **deterministic rules engine** flags known interaction pairs (prediction/classification), and a **generative-AI layer** (live Claude API with a rule-based fallback) turns that flag into a plain-language explanation a patient can act on. MVP 1 ships with only the first — the GenAI layer is an explicit Phase 2 "fast follow," not a Phase 1 requirement.
