"""Tests for src/ai_layer.py — the opt-in Phase 2 preview AI layer.

Only the deterministic fallback paths are exercised here; a live API call
needs network access and a real key and is out of scope for this suite,
same as ai_engine.py's fallback path in the full-vision app. Every test
force-disables the live client via monkeypatch so results don't depend on
whether ANTHROPIC_API_KEY happens to be set in the environment running
the tests.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src import ai_layer


def test_is_live_false_without_client(monkeypatch):
    monkeypatch.setattr(ai_layer, "_client", None)
    assert ai_layer.is_live() is False


def test_summarize_interaction_text_uses_structured_fallback_when_clinical_impact_present(monkeypatch):
    monkeypatch.setattr(ai_layer, "_client", None)
    raw = (
        "Alcohol Clinical Impact: Alcohol is known to potentiate the effect of "
        "metformin on lactate metabolism. Intervention: Warn patients against "
        "excessive alcohol intake. Insulin Secretagogues Clinical Impact: May "
        "increase the risk of hypoglycemia. Intervention: Patients may require "
        "lower doses."
    )
    rows, source = ai_layer.summarize_interaction_text(raw)
    assert source == "simulated-table"
    assert len(rows) == 2
    assert all(len(r) == 3 for r in rows)


def test_summarize_interaction_text_falls_back_to_sentence_bullets_without_structure(monkeypatch):
    monkeypatch.setattr(ai_layer, "_client", None)
    raw = "ACE-inhibitors Reports suggest NSAIDs may diminish their effect. This should be considered in patients taking both."
    rows, source = ai_layer.summarize_interaction_text(raw)
    assert source == "simulated-bullets"
    assert len(rows) >= 1
    assert all(isinstance(r, str) for r in rows)


def test_trim_words_never_cuts_mid_word():
    result = ai_layer._trim_words("this is a very long heading fragment indeed truly", max_words=8, max_chars=20)
    words = result.split()
    # every word in the trimmed result must be a whole word from the source
    assert all(w in "this is a very long heading fragment indeed truly".split() for w in words)


def test_parse_markdown_table_skips_header_and_separator_rows():
    md = (
        "| Interacts with | What can happen | What to do |\n"
        "| --- | --- | --- |\n"
        "| Alcohol | Raises lactic acidosis risk | Avoid excess alcohol |\n"
    )
    rows = ai_layer._parse_markdown_table(md)
    assert rows == [("Alcohol", "Raises lactic acidosis risk", "Avoid excess alcohol")]


def test_get_chatbot_reply_falls_back_without_client(monkeypatch):
    monkeypatch.setattr(ai_layer, "_client", None)
    reply, source = ai_layer.get_chatbot_reply("Can I drink grape juice with my medication?", ["METFORMIN"])
    assert source == "simulated"
    assert "pharmacist" in reply.lower()


def test_call_llm_returns_none_without_client(monkeypatch):
    monkeypatch.setattr(ai_layer, "_client", None)
    assert ai_layer._call_llm("system", "user") is None
