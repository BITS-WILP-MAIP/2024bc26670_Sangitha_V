"""Real, FDA-sourced drug-interaction reference text.

Loads pre-fetched openFDA drug-label "Drug Interactions" section text
(../openfda_interactions_fetcher.py in the project root fetches and caches
this — the app never calls the API live, preserving MVP 1's offline-first
design). This is deliberately NOT structured pairwise interaction data —
it's real, citable, free-text label content, most useful as reference
context for a pharmacist reviewing a drug outside the small illustrative
pairwise table in interaction_engine.py.

Important caveat, surfaced to the UI, not hidden: openFDA label records for
combination products (e.g. a multivitamin) report interactions for the
WHOLE PRODUCT'S label, which may describe a co-ingredient's interaction
rather than the searched ingredient's own. The source label name is always
shown alongside the text so this can't be silently misread as a
single-ingredient monograph.
"""

import csv


def load_fda_reference_text(csv_path):
    """Returns {ingredient: {"text": ..., "source_brand": ...}}."""
    out = {}
    try:
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ing = (row.get("ingredient") or "").strip().upper()
                if ing and row.get("drug_interactions_text"):
                    out[ing] = {
                        "text": row["drug_interactions_text"],
                        "source_brand": row.get("source_brand", "(unknown)"),
                    }
    except FileNotFoundError:
        pass
    return out


def get_reference_text(drug_name, fda_reference_map):
    """Look up real FDA reference text for a drug name (canonical or raw
    Orange Book name) by prefix match against the cached map's keys.
    Returns the {"text", "source_brand"} dict, or None if not covered."""
    if not drug_name:
        return None
    name = drug_name.strip().upper()
    for key, value in fda_reference_map.items():
        if name.startswith(key) or key.startswith(name):
            return value
    return None
