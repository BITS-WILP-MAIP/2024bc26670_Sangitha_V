# Phase 4 — Data, Model & Evaluation Strategy

## Data Sources & Feasibility

| Source | What It Provides | Access |
|---|---|---|
| DrugBank | Structured drug-drug interaction data, mechanisms, and severity | Free academic/API access; commercial licensing for production scale |
| RxNorm (NLM) | Standardized drug naming/normalization | Free public API |
| openFDA | Structured drug label data, adverse event reports (FAERS) | Free public API |
| First-party adherence & check-in data | Patient-specific adherence history for personalization | Collected directly, with explicit consent |

**What's actually wired in today:** `orange_book_dataset_generator.py` pulls the FDA's public openFDA Orange Book API directly — ~56,000 records / ~2,300 unique active ingredients — into `data/orange_book_drugs.csv`. MVP 1's medication search and matching run against this real dataset, not a hand-picked list. Interaction *pairs* remain a small, illustrative reference set (`data/orange_book_interactions.csv`) pending a licensed database (DrugBank) — the same gap named in Section 8 of the product proposal.

**Extending coverage honestly, not by fabricating pairs at scale:** rather than inventing structured interaction data for all ~2,300 ingredients (2.6M+ possible pairs — not something that can be honestly hand-authored or hallucinated for a patient-safety feature), `openfda_interactions_fetcher.py` fetches the actual "Drug Interactions" section text from openFDA's public drug label API for named ingredients, cached to `data/openfda_interaction_warnings.csv`. `mvp1/src/fda_reference.py` surfaces this real, citable text as pharmacist context whenever a drug falls outside the small pairwise table — never presented as a pairwise match, and always shown with its source label name since combination-product labels can describe a co-ingredient's interaction rather than the searched drug's own.

## The AI/Model Approach — Deliberately Not a Novel Model

Two distinct jobs, not one model:

1. **Prediction/classification (the safety-critical half):** a deterministic, rules-based lookup against a fixed interaction table. No machine learning. This is intentional — the rules are small, known, and must never silently miss a real interaction, which favors a reviewable lookup table over a learned model at this stage.
2. **Generation (the explanation half, Phase 2+):** a live LLM call (Claude API) with a rule-based fallback, used only to turn an already-determined risk flag into plain language. The generative layer never makes the safety decision — it only explains a decision the deterministic engine already made.

## Medication Identity Normalization

Real regulatory data uses salt-form ingredient names ("Amlodipine Besylate"), not the plain generic names a patient or a small interaction table use ("Amlodipine"). MVP 1 implements a simplified RxNorm-style normalizer (`mvp1/src/drug_normalizer.py`) that maps real Orange Book names to a small canonical set — tested explicitly against both correct matches and false-positive risks (`mvp1/tests/test_drug_normalizer.py`).

## Evaluation Strategy

| What's measured | How | Threshold |
|---|---|---|
| Pharmacist agreement with flagged risk level | Manual audit during the 60-day pilot | ≥ 95% |
| False-positive interaction rate | Pharmacist-audited sample | < 5% |
| Adherence rate | Check-in log vs. scheduled doses | ≥ 85% at 90 days |
| Interaction alerts acted on | Pharmacist contacted / dose adjusted | ≥ 70% |
| Pharmacist review turnaround | Time from flag to action | < 2 hours for high-risk |

Unit-test coverage (`mvp1/tests/`, 25 tests) is the code-level evaluation layer underneath these product metrics — it proves the deterministic engine behaves correctly on known cases *before* any pilot data is collected, not instead of pilot evaluation.

## Model/Data Drift

A scheduled sync with DrugBank/openFDA update cycles is the planned mitigation as new drugs and generics enter the market (Risk Register, `Risk_Note.md`). If a scanned medication has no current match, it is routed to a pharmacist rather than silently ignored — implemented and tested, not just planned.
