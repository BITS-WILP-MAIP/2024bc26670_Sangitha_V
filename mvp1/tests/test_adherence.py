"""Tests for src/adherence.py — per-drug check-in seeding and the config-driven KPI snapshot."""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.adherence import daily_adherence_pct, get_kpi_snapshot, overall_adherence_pct, seed_adherence_history
from src.config import load_config


def test_seed_adherence_history_returns_requested_number_of_days():
    log = seed_adherence_history(days=13, seed_taken_ratio=0.82, drugs=["METFORMIN"])
    assert len(log) == 13


def test_seed_adherence_history_excludes_today():
    log = seed_adherence_history(days=13, seed_taken_ratio=0.82, drugs=["METFORMIN"])
    today_iso = datetime.now().date().isoformat()
    assert today_iso not in log


def test_seed_adherence_history_is_deterministic_for_same_seed():
    a = seed_adherence_history(days=13, seed_taken_ratio=0.82, drugs=["METFORMIN", "LISINOPRIL"], seed=42)
    b = seed_adherence_history(days=13, seed_taken_ratio=0.82, drugs=["METFORMIN", "LISINOPRIL"], seed=42)
    assert a == b


def test_seed_adherence_history_has_one_entry_per_drug_per_day():
    drugs = ["METFORMIN", "LISINOPRIL", "ATORVASTATIN"]
    log = seed_adherence_history(days=5, seed_taken_ratio=0.82, drugs=drugs)
    for day_status in log.values():
        assert set(day_status.keys()) == set(drugs)
        assert all(isinstance(v, bool) for v in day_status.values())


def test_daily_adherence_pct_averages_across_drugs_for_each_day():
    log = {
        "2026-01-01": {"METFORMIN": True, "LISINOPRIL": False},
        "2026-01-02": {"METFORMIN": True, "LISINOPRIL": True},
    }
    result = daily_adherence_pct(log)
    assert result == [("2026-01-01", 50), ("2026-01-02", 100)]


def test_daily_adherence_pct_skips_days_with_no_drugs_logged():
    log = {"2026-01-01": {}}
    assert daily_adherence_pct(log) == []


def test_overall_adherence_pct_aggregates_taken_over_total():
    log = {
        "2026-01-01": {"METFORMIN": True, "LISINOPRIL": False},
        "2026-01-02": {"METFORMIN": True, "LISINOPRIL": True},
    }
    # 3 taken out of 4 total slots
    assert overall_adherence_pct(log) == 75


def test_overall_adherence_pct_empty_log_returns_zero():
    assert overall_adherence_pct({}) == 0


def test_get_kpi_snapshot_reads_thresholds_from_config():
    config = load_config()
    snapshot = get_kpi_snapshot(config)
    t = config["kpi_thresholds"]
    assert snapshot["Medication adherence rate"]["threshold"] == f"≥ {t['adherence_rate_min']:.0%}"
    assert snapshot["False-positive interaction rate"]["threshold"] == f"< {t['false_positive_rate_max']:.0%}"


def test_get_kpi_snapshot_returns_all_four_phase1_kpis():
    config = load_config()
    snapshot = get_kpi_snapshot(config)
    assert set(snapshot.keys()) == {
        "Medication adherence rate",
        "Interaction alerts acted on",
        "False-positive interaction rate",
        "Pharmacist review turnaround",
    }
