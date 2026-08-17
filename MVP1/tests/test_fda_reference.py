"""Tests for src/fda_reference.py — real FDA label reference text lookup.

This is deliberately NOT the safety-critical path (interaction_engine.py
owns that) — this module surfaces real, citable context when the small
pairwise table has nothing, and must never be confused with a pairwise
match itself.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.fda_reference import get_reference_text, load_fda_reference_text


def test_load_missing_file_returns_empty_dict():
    assert load_fda_reference_text("/nonexistent/path/does_not_exist.csv") == {}


def test_load_parses_ingredient_source_and_text(tmp_path):
    csv_path = tmp_path / "fixture.csv"
    csv_path.write_text(
        "ingredient,source_brand,drug_interactions_text\n"
        'WARFARIN,Warfarin Sodium,"Bleeding risk with NSAIDs."\n',
        encoding="utf-8",
    )
    result = load_fda_reference_text(str(csv_path))
    assert result == {"WARFARIN": {"text": "Bleeding risk with NSAIDs.", "source_brand": "Warfarin Sodium"}}


def test_load_skips_rows_with_empty_text(tmp_path):
    csv_path = tmp_path / "fixture.csv"
    csv_path.write_text(
        "ingredient,source_brand,drug_interactions_text\n"
        "VITAMIN A,Some Brand,\n",
        encoding="utf-8",
    )
    result = load_fda_reference_text(str(csv_path))
    assert result == {}


def test_get_reference_text_exact_match():
    ref_map = {"WARFARIN": {"text": "Bleeding risk.", "source_brand": "Warfarin Sodium"}}
    result = get_reference_text("WARFARIN", ref_map)
    assert result["text"] == "Bleeding risk."


def test_get_reference_text_matches_salt_form_prefix():
    # "WARFARIN SODIUM" (raw Orange Book name) should still find the
    # "WARFARIN" (canonical) cache entry, and vice versa.
    ref_map = {"WARFARIN": {"text": "Bleeding risk.", "source_brand": "Warfarin Sodium"}}
    assert get_reference_text("Warfarin Sodium", ref_map)["text"] == "Bleeding risk."


def test_get_reference_text_no_match_returns_none():
    ref_map = {"WARFARIN": {"text": "Bleeding risk.", "source_brand": "Warfarin Sodium"}}
    assert get_reference_text("ABACAVIR SULFATE", ref_map) is None


def test_get_reference_text_empty_input_returns_none():
    ref_map = {"WARFARIN": {"text": "Bleeding risk.", "source_brand": "Warfarin Sodium"}}
    assert get_reference_text("", ref_map) is None
    assert get_reference_text(None, ref_map) is None
