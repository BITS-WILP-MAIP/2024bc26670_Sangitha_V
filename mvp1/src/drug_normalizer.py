"""Medication identity — real FDA Orange Book data + RxNorm-style normalization.

Loaded from the FDA's public openFDA Orange Book API (~2,300 unique active
ingredients — see orange_book_dataset_generator.py in the project root).
Real regulatory records use salt-form names ("Amlodipine Besylate"); this
module maps those to the small set of canonical generic names MVP 1 actually
tracks interaction data for ("AMLODIPINE").
"""

import csv

# Canonical drug reference — illustrative subset for the single condition
# this MVP targets (Section 11, Phase 1): Type 2 diabetes with
# cardiometabolic comorbidities.
CANONICAL_DRUGS = {
    "METFORMIN": {"class": "Biguanide (diabetes)", "common_use": "Type 2 diabetes — lowers blood sugar", "regimen_role": "First-line therapy"},
    "LISINOPRIL": {"class": "ACE inhibitor (blood pressure)", "common_use": "Hypertension, heart failure", "regimen_role": "Add-on — blood pressure control"},
    "ATORVASTATIN": {"class": "Statin (cholesterol)", "common_use": "High cholesterol, cardiovascular risk reduction", "regimen_role": "Add-on — cardiovascular risk reduction"},
    "WARFARIN": {"class": "Anticoagulant (blood thinner)", "common_use": "Prevents blood clots", "regimen_role": "Add-on — anticoagulation"},
    "ASPIRIN": {"class": "Antiplatelet / NSAID", "common_use": "Pain relief, cardiovascular protection at low dose", "regimen_role": "Add-on — antiplatelet"},
    "IBUPROFEN": {"class": "NSAID", "common_use": "Pain and inflammation relief", "regimen_role": "As-needed — pain relief"},
    "AMLODIPINE": {"class": "Calcium channel blocker (blood pressure)", "common_use": "Hypertension", "regimen_role": "Add-on — blood pressure control"},
}


def load_orange_book_ingredients(csv_path):
    """Return a sorted list of unique, title-cased ingredient names from a
    real (or fixture) Orange Book CSV. Missing file -> empty list, not a
    crash — callers should surface that as a data-availability issue."""
    names = set()
    try:
        with open(csv_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                name = (row.get("ingredient") or "").strip()
                if name:
                    names.add(name.title())
    except FileNotFoundError:
        pass
    return sorted(names)


def normalize_to_canonical(orange_book_name):
    """Map a real, salt-form Orange Book ingredient name (e.g. 'Amlodipine
    Besylate') to its canonical generic ('AMLODIPINE'). Returns None if the
    drug isn't in the reference set this MVP tracks — callers MUST route
    that case to the pharmacist rather than silently dropping it (Section 9
    risk mitigation: an unmatched medication is never silently ignored)."""
    if not orange_book_name:
        return None
    name = orange_book_name.strip().upper()
    for canon in CANONICAL_DRUGS:
        if name.startswith(canon):
            return canon
    return None
