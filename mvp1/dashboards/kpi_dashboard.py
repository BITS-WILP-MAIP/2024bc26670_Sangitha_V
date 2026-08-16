"""KPI Dashboard — Phase 1 subset of the Metrics Framework (Section 7)."""

import pandas as pd
import streamlit as st

from src.adherence import get_kpi_snapshot

from .theme import STATUS_COLOR


def render_kpi_dashboard(config):
    theme = config["theme"]
    st.title("\U0001F4CA KPI Dashboard")
    st.caption("Live view of the Phase 1 subset of the Metrics Framework defined in the product proposal.")

    kpi_snapshot = get_kpi_snapshot(config)
    cols = st.columns(len(kpi_snapshot))
    for col, (name, kpi) in zip(cols, kpi_snapshot.items()):
        color = STATUS_COLOR[kpi["status"]]
        col.markdown(
            f"""<div class="mg-card" style="border-left-color:{color}">
            <span style="font-size:0.85rem;color:#555">{name}</span><br>
            <h2 style="color:{theme['prussian']};margin:0.1rem 0">{kpi['value']}</h2>
            <span style="font-size:0.78rem;color:#777">Threshold: {kpi['threshold']}</span></div>""",
            unsafe_allow_html=True,
        )

    df = pd.DataFrame({
        "KPI": list(kpi_snapshot.keys()),
        "Status": [k["status"].replace("_", " ").title() for k in kpi_snapshot.values()],
    })
    st.markdown("### Status summary")
    st.dataframe(df, use_container_width=True, hide_index=True)

    gates = config["acceptance_gates"]
    st.caption(
        f"Graduation gate to Phase 2 (Section 4.3): ≥ {gates['pharmacist_agreement_min']:.0%} pharmacist "
        f"agreement with flagged risk level, sustained over a {gates['pilot_duration_days']}-day pilot."
    )
