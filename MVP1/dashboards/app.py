"""MedGuardian AI — MVP 1 entry point.

Run from the mvp1/ directory: streamlit run dashboards/app.py

Strictly scoped to Phase 1 (Section 11 of the product proposal): a single
condition, one language, a rules-based interaction engine, adherence
check-ins, and a mandatory pharmacist review queue. The three core pages
(Patient Dashboard, Pharmacist Review Queue, KPI Dashboard) make zero
safety decisions via AI/LLM, by design. A separate, clearly-labeled
"Phase 2 Preview" page opts into a live Claude integration (src/ai_layer.py)
to demo the Section 2.1 GenAI explanation layer — see mvp1/README.md.
"""

import os
import sys

import streamlit as st

# Make "src" and "dashboards" importable as packages when Streamlit runs
# this file directly (mirrors the standard Streamlit multi-module pattern).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.config import load_config
from src.interaction_engine import load_interactions
from src.config import resolve_data_path
from src.state import build_patient_state

from dashboards.theme import apply_theme
from dashboards.patient_dashboard import render_patient_dashboard
from dashboards.pharmacist_queue import render_pharmacist_queue
from dashboards.kpi_dashboard import render_kpi_dashboard
from dashboards.phase2_preview import render_phase2_preview


def _init_session_state(config, interactions):
    if "patient_meds" not in st.session_state:
        for key, value in build_patient_state(config, interactions).items():
            st.session_state[key] = value


def main():
    config = load_config()

    st.set_page_config(page_title="MedGuardian AI — MVP 1", page_icon="\U0001F48A", layout="wide")
    apply_theme(config["theme"])

    interactions = load_interactions(str(resolve_data_path(config, "orange_book_interactions")))
    _init_session_state(config, interactions)

    st.sidebar.markdown("## \U0001F48A MedGuardian AI")
    st.sidebar.caption("MVP 1 — rules-based medication safety core, with an opt-in Phase 2 AI preview")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        [
            "\U0001F3E0  Patient Dashboard",
            "\U0001F9D1‍⚕️  Pharmacist Review Queue",
            "\U0001F4CA  KPI Dashboard",
            "\U0001F9EA  Phase 2 Preview (Ask MedGuardian)",
        ],
        label_visibility="collapsed",
        help="The first three pages are Phase 1 (zero AI). Phase 2 Preview opts into a live Claude integration.",
    )

    st.sidebar.markdown("---")
    if st.session_state.review_queue:
        pending = len([r for r in st.session_state.review_queue if r["status"] == "Pending pharmacist review"])
        st.sidebar.warning(f"{pending} alert(s) awaiting pharmacist review")
    else:
        st.sidebar.success("No pending review items")

    st.sidebar.caption(
        "Phase 1 pilot scope: single condition, one language, illustrative reference "
        "data. Not for real clinical use."
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(f"v{config['app']['version']} — {config['app']['phase']}")

    if page.startswith("\U0001F3E0"):
        render_patient_dashboard(config)
    elif page.startswith("\U0001F9D1"):
        render_pharmacist_queue(config)
    elif page.startswith("\U0001F4CA"):
        render_kpi_dashboard(config)
    elif page.startswith("\U0001F9EA"):
        render_phase2_preview(config)


if __name__ == "__main__":
    main()
