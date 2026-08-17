"""Tests for src/interaction_engine.py — the deterministic safety check.

This module is the entire clinical-safety surface of MVP 1. A false
negative here (missing a real interaction) is the single worst failure mode
named in the product proposal's Risk Register (Section 9), so these tests
lean toward proving detection works, not just that the code runs.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.interaction_engine import check_interactions, load_interactions

FIXTURE_INTERACTIONS = [
    ("WARFARIN", "IBUPROFEN", "high", "NSAIDs can increase bleeding risk and change INR when combined with warfarin."),
    ("LISINOPRIL", "IBUPROFEN", "moderate", "NSAIDs may reduce blood pressure control."),
    ("ASPIRIN", "IBUPROFEN", "low", "Reduces aspirin's cardioprotective effect."),
]


def test_detects_known_high_risk_pair():
    hits = check_interactions(["WARFARIN", "IBUPROFEN"], FIXTURE_INTERACTIONS)
    assert len(hits) == 1
    assert hits[0]["severity"] == "high"
    assert hits[0]["pair"] == ("WARFARIN", "IBUPROFEN")


def test_no_interaction_for_unrelated_pair():
    # Metformin has no interaction rules at all in this reference set.
    hits = check_interactions(["METFORMIN", "LISINOPRIL"], FIXTURE_INTERACTIONS)
    assert hits == []


def test_pair_order_in_med_list_does_not_matter():
    a = check_interactions(["WARFARIN", "IBUPROFEN"], FIXTURE_INTERACTIONS)
    b = check_interactions(["IBUPROFEN", "WARFARIN"], FIXTURE_INTERACTIONS)
    assert a == b


def test_case_insensitive_med_list():
    hits = check_interactions(["warfarin", "ibuprofen"], FIXTURE_INTERACTIONS)
    assert len(hits) == 1


def test_multiple_simultaneous_interactions_all_detected():
    # A patient on warfarin, lisinopril, and ibuprofen has two live risks —
    # both must surface, not just the first match found.
    hits = check_interactions(["WARFARIN", "LISINOPRIL", "IBUPROFEN"], FIXTURE_INTERACTIONS)
    severities = sorted(h["severity"] for h in hits)
    assert severities == ["high", "moderate"]


def test_single_medication_never_raises():
    assert check_interactions(["METFORMIN"], FIXTURE_INTERACTIONS) == []


def test_empty_medication_list_returns_no_hits():
    assert check_interactions([], FIXTURE_INTERACTIONS) == []


def test_load_interactions_missing_file_returns_empty_list():
    assert load_interactions("/nonexistent/path/does_not_exist.csv") == []


def test_load_interactions_normalizes_salt_form_names(tmp_path):
    csv_path = tmp_path / "fixture_interactions.csv"
    csv_path.write_text(
        "drug_a,drug_b,severity,explanation\n"
        "WARFARIN SODIUM,IBUPROFEN,high,Bleeding risk.\n",
        encoding="utf-8",
    )
    rules = load_interactions(str(csv_path))
    assert rules == [("WARFARIN", "IBUPROFEN", "high", "Bleeding risk.")]


def test_load_interactions_excludes_rows_with_unmatched_drug(tmp_path):
    # A rule referencing a drug outside the canonical set can't be checked
    # against anything — it should be silently excluded, not crash.
    csv_path = tmp_path / "fixture_interactions.csv"
    csv_path.write_text(
        "drug_a,drug_b,severity,explanation\n"
        "ABACAVIR SULFATE,IBUPROFEN,low,Not a real rule.\n"
        "WARFARIN SODIUM,ASPIRIN,high,Real rule.\n",
        encoding="utf-8",
    )
    rules = load_interactions(str(csv_path))
    assert len(rules) == 1
    assert rules[0][:2] == ("WARFARIN", "ASPIRIN")
