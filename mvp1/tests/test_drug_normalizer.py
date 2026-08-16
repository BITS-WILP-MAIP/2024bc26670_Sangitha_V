"""Tests for src/drug_normalizer.py — the RxNorm-style matching layer.

This is safety-critical: a drug that should be recognized but isn't gets
silently mis-tracked, and a drug that gets over-matched to the wrong
canonical name could suppress a real interaction alert. Both directions are
tested explicitly.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.drug_normalizer import CANONICAL_DRUGS, load_orange_book_ingredients, normalize_to_canonical


def test_normalize_exact_canonical_name():
    assert normalize_to_canonical("Lisinopril") == "LISINOPRIL"


def test_normalize_real_salt_form_name():
    # Real FDA Orange Book records use salt-form names, not bare generics.
    assert normalize_to_canonical("Amlodipine Besylate") == "AMLODIPINE"
    assert normalize_to_canonical("Warfarin Sodium") == "WARFARIN"
    assert normalize_to_canonical("Metformin Hydrochloride") == "METFORMIN"
    assert normalize_to_canonical("Atorvastatin Calcium") == "ATORVASTATIN"


def test_normalize_is_case_insensitive():
    assert normalize_to_canonical("ibuprofen") == "IBUPROFEN"
    assert normalize_to_canonical("IBUPROFEN") == "IBUPROFEN"


def test_normalize_unknown_drug_returns_none():
    # Must return None, not guess — callers route None to pharmacist review
    # rather than silently accepting an unrecognized medication.
    assert normalize_to_canonical("Abacavir Sulfate") is None


def test_normalize_empty_or_missing_input_returns_none():
    assert normalize_to_canonical("") is None
    assert normalize_to_canonical(None) is None


def test_normalize_does_not_false_positive_on_substring():
    # "Levamlodipine Maleate" starts with neither "AMLODIPINE" nor any other
    # canonical name as a true prefix once salts are stripped — guards
    # against accidentally matching a related-but-different active ingredient.
    assert normalize_to_canonical("Levamlodipine Maleate") is None


def test_every_canonical_drug_has_display_metadata():
    for name, info in CANONICAL_DRUGS.items():
        assert info.get("class"), f"{name} is missing a class label"
        assert info.get("common_use"), f"{name} is missing a common_use label"


def test_load_orange_book_ingredients_missing_file_returns_empty_list():
    assert load_orange_book_ingredients("/nonexistent/path/does_not_exist.csv") == []


def test_load_orange_book_ingredients_dedupes_and_title_cases(tmp_path):
    csv_path = tmp_path / "fixture.csv"
    csv_path.write_text(
        "ingredient,brand_name\n"
        "WARFARIN SODIUM,Coumadin\n"
        "WARFARIN SODIUM,Jantoven\n"  # duplicate ingredient, different brand
        "ASPIRIN,Bayer\n",
        encoding="utf-8",
    )
    result = load_orange_book_ingredients(str(csv_path))
    assert result == ["Aspirin", "Warfarin Sodium"]
