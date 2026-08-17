"""Phase 2 Preview — live chatbot for general medication questions.

Deliberately NOT part of the Phase 1 pilot scope (Section 11) — walled off
on its own page, with its own banner, so MVP 1's core pages (Patient
Dashboard, Pharmacist Review Queue, KPI Dashboard) keep behaving exactly as
documented: deterministic, zero-AI decisions. This page previews the
Section 2.1 GenAI explanation layer and never overrides a flagged
interaction risk — it only answers general questions.
"""

import streamlit as st

from src.ai_layer import get_chatbot_reply, is_live


def render_phase2_preview(config):
    st.title("\U0001F9EA Phase 2 Preview — Ask MedGuardian")
    st.warning(
        "This page previews a **Phase 2** capability (Section 2.1 — GenAI explanation "
        "layer) and is **not part of the Phase 1 pilot scope** defined in Section 11 of "
        "the product proposal. It is not medical advice and never overrides a flagged "
        "interaction risk — always confirm anything important with your pharmacist."
    )
    if is_live():
        st.caption("✨ Connected to a live Claude model for this session.")
    else:
        st.caption(
            "⚙️ No ANTHROPIC_API_KEY configured for this session — questions will get an "
            "explanatory message rather than a simulated medical answer, since guessing "
            "at drug-safety advice without a real model would be unsafe."
        )

    if "phase2_chat_history" not in st.session_state:
        st.session_state.phase2_chat_history = []

    for role, text in st.session_state.phase2_chat_history:
        with st.chat_message(role):
            st.write(text)

    user_message = st.chat_input("e.g. Can I drink grape juice after taking my medication?")
    if user_message:
        st.session_state.phase2_chat_history.append(("user", user_message))
        with st.chat_message("user"):
            st.write(user_message)
        reply, source = get_chatbot_reply(user_message, st.session_state.get("patient_meds", []))
        with st.chat_message("assistant"):
            st.write(reply)
            if source == "live-llm":
                st.caption("Generated live by Claude — always confirm anything important with your pharmacist.")
        st.session_state.phase2_chat_history.append(("assistant", reply))
