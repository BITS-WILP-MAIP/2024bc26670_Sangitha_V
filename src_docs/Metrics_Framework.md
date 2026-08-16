# Metrics Framework (KPI Architecture)

## Strategic Objective

Manage two linked decisions: (1) is the product actually reducing missed doses and dangerous interactions, safely, and (2) is it building the engagement and B2B traction needed to scale.

## KPI System

| KPI | Type | Decision It Supports | Owner | Threshold |
|---|---|---|---|---|
| Medication adherence rate | Outcome | Is the product delivering its core clinical value? | Clinical Lead | ≥ 85% at 90 days |
| Interaction alerts acted on | Driver | Are alerts changing behavior, not just being dismissed? | Product Lead | ≥ 70% |
| False-positive interaction rate | Quality/Driver | Is alert fatigue eroding trust? | ML Lead | < 5% |
| 30-day retention | Leading | Is the daily-use loop working? | Growth Lead | ≥ 40% |
| Pharmacist review turnaround | Leading/Operational | Is the human-in-the-loop step a bottleneck? | Clinical Ops | < 2 hours for high-risk flags |
| Adverse-event/readmission proxy reduction | Outcome (lagging) | Does this justify PBM/insurer contract renewal? | Medical Affairs | Statistically significant vs. control cohort |
| B2B pilot-to-contract conversion rate | Outcome | Is the go-to-market channel working? | BD Lead | ≥ 30% of pilots convert |

## Metrics Explicitly Removed (Vanity Metrics)

| Metric | Why Removed |
|---|---|
| Total app downloads | Doesn't indicate adherence or safety outcomes — easy to inflate, disconnected from the decisions above |
| Daily Active Users (in isolation) | A patient checking the app more isn't inherently good — what matters is whether doses are actually taken |
| Number of AI-generated explanations sent | An activity metric, not an outcome — volume says nothing about correctness or usefulness |

## Review Cadence

- **Weekly:** clinical-quality review of pharmacist-audited alerts (false-positive/negative rate) — Clinical Lead + ML Lead
- **Monthly:** product/growth review of adherence, retention, and alert-action metrics
- **Quarterly:** B2B pilot outcomes reviewed with Medical Affairs and BD for contract/renewal decisions
- **Escalation trigger:** any single missed high-risk interaction that reaches a patient without pharmacist review triggers an immediate incident review, independent of the regular cadence

## MVP 1 Subset (what's actually implemented in `config.yaml`)

MVP 1's KPI Dashboard implements the first four rows above — the patient-safety and operational metrics that are measurable from day one. The two outcome/B2B rows (readmission-proxy reduction, pilot-to-contract conversion) require real pilot data and are tracked starting Phase 3, not fabricated in the prototype.
