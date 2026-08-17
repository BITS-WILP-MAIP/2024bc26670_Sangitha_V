# PRD-Lite — MedGuardian AI

## Problem

Patients on 3+ chronic medications frequently miss doses or unknowingly combine drugs in ways that cause adverse events. This isn't a knowledge gap in medicine — it's a visibility gap between fragmented, point-in-time prescriber checks and what a patient actually takes, continuously, after leaving the pharmacy counter.

## Users

| User | What they need |
|---|---|
| Polypharmacy patient (primary) | Simple reminders, plain-language interaction warnings, reassurance not alarm |
| Pharmacist | A single queue of exactly the flags that need human judgment — nothing more |
| Health plan / PBM (buyer) | Measurable reduction in adverse events, auditable safety logs |

## Jobs-to-Be-Done

1. Tell me quickly and calmly whether a new prescription is safe with what I already take.
2. Remind me in a way that fits my routine so I don't miss or double a dose.
3. When something's risky, tell me clearly what to do and who to talk to.

## MVP 1 Scope (P0 only)

- Barcode/photo medication capture (real FDA drug data)
- Rules-based interaction engine, zero AI/LLM dependency
- Daily adherence check-in
- Mandatory pharmacist review queue
- Single condition, one language

*Explicitly out of scope for MVP 1:* GenAI explanations, caregiver dashboard, multilingual UX, personalized prediction, EHR integration, Specialty Pharma Extension. See `Product_Roadmap.md` for where each lands.

## Success Criteria

| Metric | Threshold |
|---|---|
| Pharmacist agreement with flagged risk level | ≥ 95% over 60-day pilot (graduation gate) |
| False-positive interaction rate | < 5% |
| Medication adherence rate | ≥ 85% at 90 days |
| Interaction alerts acted on | ≥ 70% |
| Pharmacist review turnaround | < 2 hours for high-risk flags |

## Non-Goals

- Not a diagnostic tool — never issues an autonomous treatment recommendation.
- Not a replacement for a doctor or pharmacist — every screen keeps a one-tap path to a human.
- Not built for real patient data yet — no auth, no encryption, illustrative interaction data only.

## Regulatory Posture

Positioned as non-SaMD wellness/decision-support, not clinical decision support — see `Risk_Note.md` for the full reasoning and the two-path timeline comparison.
