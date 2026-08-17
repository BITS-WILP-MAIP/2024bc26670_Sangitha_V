"""Deterministic, rules-based drug-drug interaction lookup.

No machine learning, no generative AI — a fixed-table lookup with mandatory
pharmacist review of anything it flags. This is the entire "AI problem
framing #1" (prediction/classification) from Section 2.1 of the product
proposal, implemented as plain code because the rules are small and known,
not learned. A real production engine needs a licensed database (DrugBank)
or openFDA's structured label/FAERS data — see Section 8.
"""

import csv

from .drug_normalizer import normalize_to_canonical


def load_interactions(csv_path):
    """Load interaction rules and normalize both sides to canonical names.
    A rule involving a drug outside the canonical set is silently excluded
    (there's nothing to match it against) rather than raising — the CSV is
    reference data, not application config."""
    rules = []
    try:
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                a = normalize_to_canonical(row["drug_a"])
                b = normalize_to_canonical(row["drug_b"])
                if a and b:
                    rules.append((a, b, row["severity"], row["explanation"]))
    except FileNotFoundError:
        pass
    return rules


def check_interactions(canonical_med_list, interactions):
    """Return interaction dicts for a list of canonical drug names against
    a given interaction rule set. Order-independent, case-insensitive."""
    found = []
    meds = {m.strip().upper() for m in canonical_med_list}
    for a, b, severity, explanation in interactions:
        if a in meds and b in meds:
            found.append({"pair": (a, b), "severity": severity, "explanation": explanation})
    return found
