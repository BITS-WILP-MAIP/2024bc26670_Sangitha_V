"""
mock_data.py
Illustrative demo dataset for MedGuardian AI.

NOTE: This is a small, hand-curated dataset for prototype/demo purposes only.
It is NOT a substitute for a live DrugBank / RxNorm / openFDA integration and
must never be used for real clinical decisions. See README.md.
"""

from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Medication reference data (illustrative subset only)
# ---------------------------------------------------------------------------
MEDICATIONS_DB = {
    "metformin": {
        "class": "Biguanide (diabetes)",
        "common_use": "Type 2 diabetes — lowers blood sugar",
    },
    "lisinopril": {
        "class": "ACE inhibitor (blood pressure)",
        "common_use": "Hypertension, heart failure",
    },
    "atorvastatin": {
        "class": "Statin (cholesterol)",
        "common_use": "High cholesterol, cardiovascular risk reduction",
    },
    "warfarin": {
        "class": "Anticoagulant (blood thinner)",
        "common_use": "Prevents blood clots",
    },
    "aspirin": {
        "class": "Antiplatelet / NSAID",
        "common_use": "Pain relief, cardiovascular protection at low dose",
    },
    "ibuprofen": {
        "class": "NSAID",
        "common_use": "Pain and inflammation relief",
    },
    "amlodipine": {
        "class": "Calcium channel blocker (blood pressure)",
        "common_use": "Hypertension",
    },
    "levothyroxine": {
        "class": "Thyroid hormone replacement",
        "common_use": "Hypothyroidism",
    },
}

# (drug_a, drug_b, severity: "low"|"moderate"|"high", plain-language explanation)
INTERACTIONS = [
    ("warfarin", "aspirin", "high",
     "Both affect blood clotting. Taking them together significantly raises bleeding risk."),
    ("warfarin", "ibuprofen", "high",
     "NSAIDs like ibuprofen can increase bleeding risk when combined with warfarin."),
    ("lisinopril", "ibuprofen", "moderate",
     "NSAIDs can reduce how well ACE inhibitors control blood pressure and may affect kidney function."),
    ("amlodipine", "atorvastatin", "moderate",
     "This combination can raise statin levels in the blood — usually manageable, but worth a pharmacist check on dose."),
    ("aspirin", "ibuprofen", "low",
     "Taking these together regularly can reduce aspirin's heart-protective effect and add stomach irritation risk."),
]


def check_interactions(med_list):
    """Return a list of interaction dicts for the given (lowercased) medication list."""
    found = []
    meds = [m.strip().lower() for m in med_list]
    for a, b, severity, explanation in INTERACTIONS:
        if a in meds and b in meds:
            found.append({"pair": (a, b), "severity": severity, "explanation": explanation})
    return found


# ---------------------------------------------------------------------------
# Demo patient
# ---------------------------------------------------------------------------
DEMO_PATIENT = {
    "name": "Asha Rao",
    "age": 62,
    "condition_summary": "Type 2 diabetes, hypertension, high cholesterol",
    "medications": ["metformin", "lisinopril", "atorvastatin", "ibuprofen"],
}


def generate_adherence_log(days=14, seed_taken_ratio=0.82):
    import random
    random.seed(42)
    log = []
    today = datetime.now()
    for i in range(days, 0, -1):
        d = today - timedelta(days=i)
        taken = random.random() < seed_taken_ratio
        log.append({"date": d.strftime("%b %d"), "taken": taken})
    return log


# ---------------------------------------------------------------------------
# KPI snapshot (matches the Metrics Framework in the product proposal)
# ---------------------------------------------------------------------------
KPI_SNAPSHOT = {
    "Medication adherence rate": {"value": "87%", "threshold": "\u2265 85%", "status": "on_track"},
    "Interaction alerts acted on": {"value": "74%", "threshold": "\u2265 70%", "status": "on_track"},
    "False-positive interaction rate": {"value": "4.1%", "threshold": "< 5%", "status": "on_track"},
    "30-day retention": {"value": "36%", "threshold": "\u2265 40%", "status": "at_risk"},
    "Pharmacist review turnaround": {"value": "1.6 hrs", "threshold": "< 2 hrs", "status": "on_track"},
}

# ---------------------------------------------------------------------------
# AI-managed Project Management artifacts (roadmap / risk register / backlog)
# ---------------------------------------------------------------------------
ROADMAP = [
    {"phase": "Phase 1 \u2014 MVP", "window": "Months 1\u20134",
     "status": "In progress", "pct_complete": 65,
     "focus": "Rules-based interaction engine, adherence reminders, pharmacist review queue"},
    {"phase": "Phase 2 \u2014 GenAI layer & expansion", "window": "Months 5\u20138",
     "status": "Not started", "pct_complete": 0,
     "focus": "Auto-generated explanations for low-risk alerts, multilingual UX"},
    {"phase": "Phase 3 \u2014 B2B distribution", "window": "Months 9\u201314",
     "status": "Not started", "pct_complete": 0,
     "focus": "PBM/health-plan pilot, caregiver dashboard, regulatory review"},
    {"phase": "Phase 4 \u2014 Scale & integration", "window": "Months 15+",
     "status": "Not started", "pct_complete": 0,
     "focus": "EHR/pharmacy API integration, personalized adherence-risk model"},
]

RISK_REGISTER = [
    {"risk": "Unreviewed high-risk interaction reaches a patient", "likelihood": "Low",
     "impact": "Severe", "owner": "Clinical Lead", "status": "Mitigated \u2014 mandatory pharmacist review live"},
    {"risk": "Regulatory classification as SaMD", "likelihood": "Medium",
     "impact": "High", "owner": "Regulatory Counsel", "status": "In review"},
    {"risk": "Health data privacy breach", "likelihood": "Low-Medium",
     "impact": "Severe", "owner": "Security Lead", "status": "Audit scheduled"},
    {"risk": "Model/data drift as new drugs enter market", "likelihood": "Medium",
     "impact": "Medium", "owner": "ML Lead", "status": "Monitoring — sync job pending"},
    {"risk": "Low adoption among low-digital-literacy patients", "likelihood": "Medium",
     "impact": "Medium", "owner": "UX Lead", "status": "Usability testing scheduled"},
]

BACKLOG = [
    {"item": "Barcode/photo medication capture", "priority": "P0", "status": "Done"},
    {"item": "Interaction alert + pharmacist review queue", "priority": "P0", "status": "Done"},
    {"item": "Daily adherence check-in & reminders", "priority": "P0", "status": "In progress"},
    {"item": "GenAI plain-language explanations", "priority": "P1", "status": "Not started"},
    {"item": "Caregiver dashboard", "priority": "P1", "status": "Not started"},
    {"item": "Personalized adherence-risk prediction", "priority": "P2", "status": "Not started"},
    {"item": "EHR/pharmacy API integration", "priority": "P2", "status": "Not started"},
]

# ---------------------------------------------------------------------------
# Specialty Pharma Extension — physician view + pharma program insights
# (illustrative only; closes the physician → patient → pharmacist → pharma loop
#  described in Section 13 of the product proposal)
# ---------------------------------------------------------------------------
SPECIALTY_PROGRAM = {
    "drug_name": "Adalimumab (specialty biologic)",
    "indication": "Rheumatoid arthritis / Crohn's disease",
    "monthly_cost": "$5,800",
    "program_name": "Specialty Care Support Program — Adalimumab",
}

PHYSICIAN_PANEL = [
    {"name": "Asha Rao", "med": "Adalimumab + metformin, lisinopril, atorvastatin",
     "adherence_pct": 93, "last_flag": "Moderate (resolved)", "status": "Stable"},
    {"name": "David Chen", "med": "Adalimumab + ibuprofen (as-needed)",
     "adherence_pct": 61, "last_flag": "High — pending pharmacist review", "status": "At risk"},
    {"name": "Priya Nair", "med": "Adalimumab only",
     "adherence_pct": 88, "last_flag": "None", "status": "Stable"},
    {"name": "Michael Osei", "med": "Adalimumab + warfarin",
     "adherence_pct": 74, "last_flag": "High — resolved by pharmacist", "status": "Watch"},
]

PHARMA_INSIGHTS = {
    "enrolled_patients": 1240,
    "avg_adherence_rate": "81%",
    "discontinuation_risk_high": 96,
    "interaction_flags_resolved_90d": 214,
    "pharmacist_escalations_90d": 58,
    "est_doses_saved_90d": 3100,
}

PHARMA_ADHERENCE_TREND = [
    {"month": "Mar", "adherence_pct": 76},
    {"month": "Apr", "adherence_pct": 77},
    {"month": "May", "adherence_pct": 79},
    {"month": "Jun", "adherence_pct": 78},
    {"month": "Jul", "adherence_pct": 80},
    {"month": "Aug", "adherence_pct": 81},
]
