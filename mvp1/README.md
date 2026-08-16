# MedGuardian AI — MVP 1

The strictly-scoped Phase 1 build, per Section 11 of the product proposal.
This is **not** the full-vision demo (that's in the project root) — it's
exactly what would ship first to a pilot clinic or PBM, and nothing more.

Structured as a config-driven, modular, tested application — `src/` for
business logic, `dashboards/` for the UI, `tests/` for pytest coverage of
the safety-critical paths, `config.yaml` for every product threshold —
rather than one monolithic script, so each layer can be reviewed and tested
independently.

See `../MVP1_Specification.docx` for the full spec: scope, acceptance
criteria, regulatory posture, and what's explicitly deferred to later phases.

## Why this folder is separate from the root app

The root `app.py` demonstrates the full product vision — GenAI explanations,
the Specialty Pharma Extension, AI-generated PM reporting — useful for
showing investors and stakeholders where the product is headed. This folder
is different on purpose: it's what Phase 1 actually is, trimmed to exactly
the RICE P0 items (Section 6) and nothing else, so it can be handed to a
pilot partner or a regulatory reviewer as a scoped, honest artifact.

## Zero AI/LLM dependency in the Phase 1 core — plus an opt-in Phase 2 preview

The three Phase 1 pages — Patient Dashboard's interaction checks, Pharmacist
Review Queue, KPI Dashboard — make **no safety decision via any LLM**. Every
interaction flag is a deterministic lookup against a fixed table
(`src/interaction_engine.py`). This is a direct expression of the RICE
table in the proposal: GenAI plain-language explanations are marked
**P1 — Fast follow**, not P0.

At the user's explicit request, two Phase 2 capabilities were added on top
of that core, isolated in `src/ai_layer.py` (imported by nothing in the
safety-critical path):

1. **FDA label summarization** (Patient Dashboard) — the real openFDA label
   text (`fda_reference.py`) is dense regulatory prose, so it's turned into
   a short table before display: live by Claude when `ANTHROPIC_API_KEY` is
   set, or a deterministic regex reformat otherwise (never a fabricated
   summary — the fallback only reorganizes text already in the source).
2. **"Phase 2 Preview — Ask MedGuardian"** (`dashboards/phase2_preview.py`)
   — a separate, clearly-labeled page for general medication questions
   (e.g. food/drug interactions like grapefruit or alcohol) that Phase 1's
   fixed table doesn't cover. Walled off from the three core pages so they
   keep behaving exactly as documented above.

Both paths go through `_call_llm()`, which returns `None` on any failure or
missing key — callers always have a safe, honest fallback, never a guess.
Without a key, the chatbot says so explicitly rather than simulating medical
advice. See `.env.example` for setup; nothing here is required to run or
test the Phase 1 core.

## Structure

```
config.yaml              Every product threshold — acceptance gates, KPI
                          thresholds, adherence seeding, theme colors
src/
  config.py               Loads config.yaml; resolves data paths
  drug_normalizer.py       Real FDA drug data + RxNorm-style name matching
  interaction_engine.py    Deterministic interaction lookup — the safety core
  adherence.py             Demo patient, per-drug check-in seeding, config-driven KPIs
  fda_reference.py         Real openFDA label interaction text (reference only, not pairwise)
  state.py                 Shared patient-state builder — used at first load and on reset
  ai_layer.py              Opt-in Phase 2 preview — live Claude + deterministic fallback, isolated from the safety core
dashboards/
  app.py                   Entry point / router — run this with Streamlit
  theme.py                 Shared Sandoz-blue styling
  patient_dashboard.py      Medication capture/removal, regimen view, per-drug check-in
  pharmacist_queue.py       Human-in-the-loop review queue
  kpi_dashboard.py          Phase 1 metrics, thresholds pulled from config
  phase2_preview.py         Walled-off Phase 2 chatbot page — not part of the Phase 1 pilot scope
tests/
  test_drug_normalizer.py   Real-data normalization, incl. false-positive guards
  test_interaction_engine.py  Detection, multi-drug lists, malformed data
  test_adherence.py         Per-drug check-in seeding, config-driven KPI snapshot
  test_fda_reference.py     Real FDA label reference text parsing/matching
  test_state.py             Reset/first-load state builder is reproducible
  test_ai_layer.py          Deterministic fallback paths for the Phase 2 preview layer
```

## Patient Dashboard capabilities

- **Remove a medication** — each medication card has its own "✕ Remove"
  button. Removing a drug also drops any pending interaction alert that
  named it (an alert about a drug you're no longer taking no longer
  applies), but leaves past check-in history untouched.
- **Reset to demo defaults** — restores the demo patient's medication list,
  interaction alerts, and adherence history in one click, useful after
  experimenting with adds/removes.
- **Per-drug daily check-in** — "Today's check-in" asks which *specific*
  medications were taken today (one checkbox per active drug, defaulting to
  taken), not a single yes/no for the whole day. `src/adherence.py` stores
  this as `{date: {drug: bool}}`.
- **Current regimen — combination therapy view** — a table and stacked bar
  chart showing the active medication combination grouped by illustrative
  "role in regimen" (e.g. first-line vs. add-on), tagged in
  `src/drug_normalizer.py`'s `CANONICAL_DRUGS`. Explicitly labeled as
  illustrative reference data, not clinical guidance.
- **14-day adherence chart** — now has labeled axes (Date / Adherence % of
  medications taken) and plots the per-day average across all drugs logged
  that day via `daily_adherence_pct()`.

## What's real vs. illustrative in the data

- **Medication identity is real.** `../data/orange_book_drugs.csv` is
  ~56,000 records / ~2,300 unique active ingredients fetched from the FDA's
  public openFDA Orange Book API (`orange_book_dataset_generator.py` in the
  project root). The "Add a medication" search and the simulated photo
  capture both search this real list — not a hand-picked handful of names.
- **Interaction pairs are still illustrative.** A real production interaction
  engine needs a licensed database (DrugBank) or openFDA's structured
  label/FAERS data — see Section 8 of the product proposal.
- **Real FDA label interaction text supplements the small pairwise table.**
  `../openfda_interactions_fetcher.py` fetches the actual "Drug Interactions"
  section text from openFDA's public drug label API (`../data/openfda_interaction_warnings.csv`,
  cached — the app never calls this API live). This is real, citable
  reference content, not structured pair data, shown to give a pharmacist
  something genuine to read — **especially for a drug outside the 7-entry
  pairwise table**, where it appears alongside the "routed to pharmacist"
  message instead of nothing. Combination-product labels (e.g. a
  multivitamin) are always shown with their source brand name, since the
  text may describe a co-ingredient's interaction rather than the searched
  drug's own — see `src/fda_reference.py`'s docstring for a concrete example
  (Vitamin A / pyridoxine).
- **A medication with no interaction data is never silently added as "safe."**
  If a real, FDA-listed drug isn't in the small reference interaction set,
  it's explicitly routed to the pharmacist queue instead — this is the
  literal implementation of the Section 9 risk mitigation ("automated alert
  if a scanned medication has no current match, routed to pharmacist rather
  than silently ignored"), and it's covered by
  `test_interaction_engine.py::test_load_interactions_excludes_rows_with_unmatched_drug`.

## Run it

```bash
cd mvp1
pip install -r requirements.txt
streamlit run dashboards/app.py
```

Or just `./run.sh` (macOS/Linux) or `run_mvp1.bat` (Windows) from this folder.

To try the live Phase 2 preview (FDA summarization + chatbot), copy
`.env.example` to `.env` and add your own `ANTHROPIC_API_KEY` — never commit
the real `.env` file or paste a real key into chat/docs. Without it, both
features still work via their deterministic fallback.

## Run the tests

```bash
cd mvp1
pytest tests/ -v
```

Every test exercises real behavior against real or fixture data — no
mocked-out safety logic. `test_interaction_engine.py` in particular is the
regression suite for the single most important guarantee in the product:
a known interaction is never missed, and an unrecognized drug is never
silently treated as safe.
