"""Demo patient, adherence history seeding, and the KPI snapshot.

KPI thresholds are read from config.yaml (Section 7 of the product
proposal), not hardcoded — the dashboard displays whatever the config
actually says the bar is, so the two can never silently drift apart.
"""

import random
from datetime import datetime, timedelta

DEMO_PATIENT = {
    "name": "Asha Rao",
    "age": 62,
    "condition_summary": "Type 2 diabetes with cardiometabolic comorbidities (hypertension, high cholesterol)",
    "medications": ["METFORMIN", "LISINOPRIL", "ATORVASTATIN", "IBUPROFEN"],
}

# Illustrative current values (a real deployment reads these from a live
# adherence/alerts backend, not a constant).
_ILLUSTRATIVE_VALUES = {
    "Medication adherence rate": "87%",
    "Interaction alerts acted on": "74%",
    "False-positive interaction rate": "4.1%",
    "Pharmacist review turnaround": "1.6 hrs",
}


def get_kpi_snapshot(config):
    """Build the KPI snapshot dict, with thresholds sourced from
    config['kpi_thresholds'] rather than hardcoded per KPI."""
    t = config["kpi_thresholds"]
    specs = [
        ("Medication adherence rate", f"≥ {t['adherence_rate_min']:.0%}"),
        ("Interaction alerts acted on", f"≥ {t['alerts_acted_on_min']:.0%}"),
        ("False-positive interaction rate", f"< {t['false_positive_rate_max']:.0%}"),
        ("Pharmacist review turnaround", f"< {t['pharmacist_review_turnaround_hours_max']} hrs"),
    ]
    snapshot = {}
    for name, threshold in specs:
        value = _ILLUSTRATIVE_VALUES[name]
        snapshot[name] = {"value": value, "threshold": threshold, "status": "on_track"}
    return snapshot


def seed_adherence_history(days, seed_taken_ratio, drugs, seed=42):
    """Seed per-drug check-in history for the days *before* today only —
    today is logged interactively via the check-in UI, not pre-generated.
    Returns {date_iso: {drug: bool}}, one entry per drug the patient was on
    that day, so the dashboard can show which specific medication was
    missed rather than only a single yes/no for the whole day."""
    rng = random.Random(seed)
    log = {}
    today = datetime.now().date()
    for i in range(days, 0, -1):
        d = today - timedelta(days=i)
        log[d.isoformat()] = {drug: rng.random() < seed_taken_ratio for drug in drugs}
    return log


def daily_adherence_pct(log):
    """Return a sorted list of (date_iso, pct_taken) across all drugs logged
    that day — the per-day series the adherence chart plots. Skips any day
    with no drugs logged (e.g. a day before any medication was added)."""
    out = []
    for date_iso, drug_status in sorted(log.items()):
        if not drug_status:
            continue
        pct = round(100 * sum(1 for v in drug_status.values() if v) / len(drug_status))
        out.append((date_iso, pct))
    return out


def overall_adherence_pct(log):
    """Aggregate taken/total across every drug and every day in the log —
    the single number shown on the 'Adherence (14 days)' stat card."""
    total = taken = 0
    for drug_status in log.values():
        total += len(drug_status)
        taken += sum(1 for v in drug_status.values() if v)
    return round(100 * taken / total) if total else 0
