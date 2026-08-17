"""Shared patient-session initialization.

Used at both app startup and an explicit "reset to demo defaults" action, so
the two paths build identical state instead of drifting apart over time.
"""

from .adherence import DEMO_PATIENT, seed_adherence_history
from .interaction_engine import check_interactions


def build_patient_state(config, interactions):
    """Return a fresh {patient_meds, review_queue, adherence_log,
    today_logged} dict seeded from the demo patient."""
    patient_meds = list(DEMO_PATIENT["medications"])
    hits = check_interactions(patient_meds, interactions)
    review_queue = [
        {**h, "status": "Pending pharmacist review"} for h in hits if h["severity"] in ("moderate", "high")
    ]
    a = config["adherence"]
    adherence_log = seed_adherence_history(a["seed_days"], a["seed_taken_ratio"], patient_meds)
    return {
        "patient_meds": patient_meds,
        "review_queue": review_queue,
        "adherence_log": adherence_log,
        "today_logged": False,
    }
