# Phase 3 — UX, Workflow & Trust Design

## Core Experience

- **Medication capture:** photo/barcode scan of a prescription label or pill bottle, auto-matched against a real drug reference dataset rather than manual free-text entry.
- **Daily check-in:** a single, low-friction tap ("Taken" / "Skipped" / "Remind me later") rather than a form.
- **Interaction alert card:** plain-language explanation ("These two together can raise your risk of dizziness — here's why, and what to do"), with a one-tap "Talk to a pharmacist" escalation.
- **Explainability panel:** every AI-generated explanation carries a "Why am I seeing this?" expandable section showing the underlying source (e.g., openFDA label data) — building trust and satisfying the explainability-in-UX principle.
- **Caregiver view:** a permissioned, read-only dashboard for a family member, with its own consent flow (Phase 2).

## Designing for Uncertainty

Interaction risk is shown as a three-tier plain-language band (**Low / Moderate / Talk to your pharmacist**) rather than a raw probability score — patients act on clear guidance, not confidence intervals. Any output the model is not confident about is routed to the pharmacist-review queue rather than shown directly to the patient, consistent with the human-in-the-loop MVP design.

## Trust & Transparency

- Every alert cites its data source (e.g., "Based on FDA label data") rather than presenting AI output as an unattributed fact.
- The app is explicit that it does not replace a doctor or pharmacist, with a persistent, one-tap path to a human.
- An unmatched medication (one the reference dataset doesn't recognize) is **never silently treated as safe** — it is explicitly routed to the pharmacist queue instead. This is implemented, not just designed: see `mvp1/tests/test_interaction_engine.py::test_load_interactions_excludes_rows_with_unmatched_drug`.

## User Flows (as built in MVP 1)

**Add a medication:** Patient opens Scan or Search → confirms the matched drug → system runs the interaction check against their current list → no risk: added immediately; moderate/high risk: patient sees the plain-language reason and the item is simultaneously routed to the pharmacist queue; unmatched drug: patient is told it isn't yet in the reference set and it is routed to the pharmacist.

**Daily check-in:** Patient taps Taken, Skipped, or Remind me later once per day — no form, no LLM call, a single state write.

**Pharmacist review:** Pharmacist sees every pending item with severity, the drugs involved (or the unmatched drug name), and the reference explanation, and can Approve to patient or Dismiss as a false positive.

See `Wireframes_and_Screens.md` for a screen-by-screen breakdown of what was actually built.
