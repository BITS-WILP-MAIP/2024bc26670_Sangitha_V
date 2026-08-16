# Phase 1 — Topic Approval & Strategy

## Business Problem → AI Problem

**Business problem:** Patients on multiple chronic medications frequently miss doses or unknowingly combine drugs in ways that cause adverse events, driving avoidable ER visits and non-adherence-related disease progression.

**AI problem framing:**
1. **A prediction/classification problem** — given a patient's current medication list, dosing history, and a candidate new prescription, predict interaction risk and adherence-drop-off risk.
2. **A generative problem** — translate structured interaction/adherence data into a plain-language, personalized explanation and nudge.

## Why Isn't This Already Solved?

This is the single most important question a reviewer will ask, so it's answered explicitly rather than left implicit:

A prescribing physician and a dispensing pharmacist each check interactions against the medication list they know about, **at a single moment** — prescribing or dispensing. Neither has continuous visibility into what a patient adds afterward:

- **The OTC & supplement blind spot** — a physician has no visibility into the ibuprofen, antacid, or supplement a patient bought on their own. The single largest source of unrecognized interactions.
- **Fragmented prescribers** — a cardiologist, an endocrinologist, and a GP each prescribe independently. Without a unified record, no single check ever sees the combined list.
- **Point-in-time, not continuous** — a prescriber checks interactions once, against the list known at that moment. What the patient adds over the following weeks is invisible until the next visit.
- **Knowledge ≠ adherence** — even a warning given correctly, once, in a rushed visit, rarely survives weeks of unsupervised daily dosing without reinforcement at the moment of risk.

The gap this product closes is not a knowledge gap in medicine — it's a **visibility gap** between fragmented, point-in-time checks and what a patient is actually taking, continuously, after they leave the pharmacy counter.

*Honest limitation, stated up front:* the MVP's actual fix is patient self-report, continuously reinforced and cross-checked — a real improvement over a once-per-visit conversation, but only as complete as what the patient remembers to log. A fully automatic reconciliation across every prescriber's system requires the same hard EHR-integration problem deferred to Phase 4.

## AI Opportunity Matrix (Value vs. Feasibility)

| Dimension | Assessment |
|---|---|
| Business value | High — addresses a top-3 driver of preventable hospital readmission; strong willingness-to-pay from health plans/PBMs who bear readmission cost |
| AI feasibility | High for MVP — core interaction logic runs on existing open pharmacological datasets without training a novel model; the GenAI explanation layer is a thin wrapper, not a research problem |
| Data availability | High — DrugBank, RxNorm, and openFDA are free, structured, and API-accessible today |
| Placement | **Quadrant: High Value / High Feasibility** — prioritize as a near-term build, not a long-horizon bet |

## Build vs. Buy vs. API Strategy

| Component | Decision | Rationale |
|---|---|---|
| Drug interaction & label data | Buy / API | Use DrugBank, RxNorm (NLM), and openFDA rather than building a pharmacological database from scratch |
| Interaction reasoning + risk scoring | Build | Proprietary layer combining patient-specific factors is the product's core IP |
| Explanation / conversational layer | Buy foundation model + Build guardrails | Use a general-purpose LLM API for language generation; build the clinical-safety prompt layer and human-review workflow in-house |
| Distribution | Partner | Go to market via health plans/PBMs and pharmacy chains rather than pure direct-to-consumer acquisition |

## Feasibility Reality Check — What's Actually Buildable Now

| Feasible now | Not feasible near-term (correctly deferred) |
|---|---|
| Rules-based interaction lookup on real DrugBank/RxNorm/openFDA data | Personalized adherence-risk *prediction* — needs real usage data at scale |
| Daily adherence check-in/reminders — pure wellness feature, no regulatory gate | EHR/pharmacy system integration — enterprise sales & security cycle independent of readiness |
| GenAI plain-language explanations with mandatory pharmacist review | Full SaMD/510(k) clearance — deliberately avoided by design |
| Non-SaMD wellness/adherence positioning — launchable without FDA premarket clearance | Physician View + Pharma Program Insights at real scale — needs a real physician data-sharing agreement and a pharma manufacturer contract |
