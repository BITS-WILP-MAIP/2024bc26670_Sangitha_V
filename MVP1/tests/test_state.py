"""Tests for src/state.py — the shared initial/reset patient state builder."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.adherence import DEMO_PATIENT
from src.config import load_config, resolve_data_path
from src.interaction_engine import load_interactions
from src.state import build_patient_state


def _config_and_interactions():
    config = load_config()
    interactions = load_interactions(str(resolve_data_path(config, "orange_book_interactions")))
    return config, interactions


def test_build_patient_state_returns_demo_medications():
    config, interactions = _config_and_interactions()
    state = build_patient_state(config, interactions)
    assert state["patient_meds"] == list(DEMO_PATIENT["medications"])


def test_build_patient_state_seeds_adherence_log_for_every_demo_drug():
    config, interactions = _config_and_interactions()
    state = build_patient_state(config, interactions)
    for day_status in state["adherence_log"].values():
        assert set(day_status.keys()) == set(DEMO_PATIENT["medications"])


def test_build_patient_state_today_logged_is_false():
    config, interactions = _config_and_interactions()
    state = build_patient_state(config, interactions)
    assert state["today_logged"] is False


def test_build_patient_state_is_reproducible():
    config, interactions = _config_and_interactions()
    a = build_patient_state(config, interactions)
    b = build_patient_state(config, interactions)
    assert a == b
