"""
openfda_interactions_fetcher.py

Fetches REAL, FDA-sourced drug-interaction warning text from openFDA's
public drug label API (/drug/label.json, field: drug_interactions) — the
actual "Drug Interactions" section of the FDA-approved label, not a
fabricated or inferred claim.

This is deliberately NOT a source of structured drug-pair + severity data
(that requires a licensed database like DrugBank — see Section 8 of the
product proposal). It's a source of real, citable, free-text reference
context per drug, used to give a pharmacist something genuine to read for
a medication outside the small illustrative pairwise interaction table
(mvp1/src/interaction_engine.py), instead of nothing.

Run once (or re-run to refresh); output is cached to CSV and read by the
app at runtime — the app itself never calls this API live, preserving
MVP 1's offline-first, zero-external-call-at-runtime design.

Usage:
    python openfda_interactions_fetcher.py
"""

import csv
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

API_URL = "https://api.fda.gov/drug/label.json"
DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_PATH = DATA_DIR / "openfda_interaction_warnings.csv"

# The canonical drug set MVP 1 currently recognizes (Section 11, single
# condition), plus Vitamin A — added here specifically because it's a real,
# commonly-taken OTC supplement with no entry in the small illustrative
# pairwise table, and is the drug that surfaced this gap.
SUBSTANCE_NAMES = [
    "METFORMIN",
    "LISINOPRIL",
    "ATORVASTATIN",
    "WARFARIN",
    "ASPIRIN",
    "IBUPROFEN",
    "AMLODIPINE",
    "VITAMIN A",
]

MAX_CHARS = 4000  # keep the CSV reasonable; UI truncates further for display


MIN_SUBSTANTIVE_CHARS = 60  # below this, a result is usually just a bare
# section header ("Drug Interactions") with no real body text — not worth
# surfacing as if it were real reference content.


def fetch_interaction_text(substance_name, candidates=5, retries=3):
    """Query openFDA for up to `candidates` label records with a non-empty
    drug_interactions field for this substance, and return the most
    substantive one (longest text, above a minimum length) rather than
    blindly taking the first match — some labels populate only the section
    header with no body. Returns (text, brand) or (None, None) if nothing
    substantive is found."""
    query = f'openfda.substance_name:"{substance_name}"+AND+_exists_:drug_interactions'
    url = f"{API_URL}?search={quote(query, safe='+:\"')}&limit={candidates}"
    for attempt in range(retries):
        try:
            with urlopen(url, timeout=30) as response:
                payload = json.load(response)
            results = payload.get("results", [])
            if not results:
                return None, None
            best_text, best_brand = None, None
            for record in results:
                text_blocks = record.get("drug_interactions", [])
                text = " ".join(text_blocks)[:MAX_CHARS].strip()
                if len(text) >= MIN_SUBSTANTIVE_CHARS and (best_text is None or len(text) > len(best_text)):
                    best_text = text
                    best_brand = (record.get("openfda", {}).get("brand_name") or ["(generic)"])[0]
            return best_text, best_brand
        except HTTPError as e:
            if e.code == 404:
                return None, None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None, None


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in SUBSTANCE_NAMES:
        print(f"Fetching real FDA label interaction text for {name}...")
        text, brand = fetch_interaction_text(name)
        if text:
            rows.append({"ingredient": name, "source_brand": brand, "drug_interactions_text": text})
            print(f"  found ({len(text)} chars, source label: {brand})")
        else:
            print("  no drug_interactions field found for this substance")
        time.sleep(1.0)  # be polite to the public, unauthenticated rate limit

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ingredient", "source_brand", "drug_interactions_text"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} real FDA interaction-warning records to {OUT_PATH}")
    print(
        "\nTo extend coverage beyond this starter set: add more substance names to "
        "SUBSTANCE_NAMES and re-run. Scaling to the full ~2,300-ingredient Orange "
        "Book list is the same script run longer, respecting openFDA's public rate "
        "limit (40 req/min, 1,000/day unauthenticated) — a data-engineering task, "
        "not a content-fabrication one."
    )


if __name__ == "__main__":
    main()
