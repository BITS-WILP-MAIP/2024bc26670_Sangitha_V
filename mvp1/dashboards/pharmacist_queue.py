"""Pharmacist Review Queue — the human-in-the-loop gate (Section 4.3)."""

import streamlit as st

from .theme import SEVERITY_COLOR


def render_pharmacist_queue(config):
    st.title("\U0001F9D1‍⚕️ Pharmacist Review Queue")
    st.caption("Every moderate/high-risk flag — including unmatched medications — is held here until a pharmacist actions it.")

    if not st.session_state.review_queue:
        st.success("Queue is empty.")

    for i, item in enumerate(st.session_state.review_queue):
        a, b = item["pair"]
        color = SEVERITY_COLOR[item["severity"]]
        with st.container():
            st.markdown(
                f"""<div class="mg-card" style="border-left-color:{color}">
                <span class="mg-badge" style="background-color:{color}">{item['severity'].upper()}</span>
                &nbsp;<b>{str(a).title()} + {str(b).title()}</b><br>
                <span style="color:#555">{item['explanation']}</span><br><br>
                <i>Status: {item['status']}</i></div>""",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            if item["status"] == "Pending pharmacist review":
                if c1.button("Approve alert to patient", key=f"approve_{i}"):
                    st.session_state.review_queue[i]["status"] = "Approved — sent to patient"
                    st.rerun()
                if c2.button("Dismiss (false positive)", key=f"dismiss_{i}"):
                    st.session_state.review_queue[i]["status"] = "Dismissed by pharmacist"
                    st.rerun()
