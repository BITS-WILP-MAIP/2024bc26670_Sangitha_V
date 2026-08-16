"""
MedGuardian AI \u2014 clickable MVP
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from mock_data import (
    MEDICATIONS_DB, DEMO_PATIENT, generate_adherence_log, check_interactions,
    KPI_SNAPSHOT, ROADMAP, RISK_REGISTER, BACKLOG,
    SPECIALTY_PROGRAM, PHYSICIAN_PANEL, PHARMA_INSIGHTS, PHARMA_ADHERENCE_TREND,
)
from ai_engine import get_copilot_reply, generate_pm_summary, generate_pharma_insights_summary

# ---------------------------------------------------------------------------
# Theme: Sandoz blue palette
# ---------------------------------------------------------------------------
DENIM = "#0A53BE"        # primary
PRUSSIAN = "#001C4A"     # dark / headers
CORNFLOWER = "#94BFE7"   # secondary / accents
ANAKIWA = "#A8D5FF"      # light accent
PAMPAS = "#F1ECE9"       # warm neutral background
WHITE = "#FFFFFF"

SEVERITY_COLOR = {"low": "#3E8E5B", "moderate": "#D98A0D", "high": "#C0392B"}
STATUS_COLOR = {"on_track": "#3E8E5B", "at_risk": "#D98A0D", "off_track": "#C0392B"}

st.set_page_config(page_title="MedGuardian AI", page_icon="\U0001F48A", layout="wide")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {PAMPAS};
        color: {PRUSSIAN};
    }}
    .stApp p, .stApp li, .stApp span, .stApp label, .stApp div,
    .stMarkdown, .stMarkdown p, [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p, .stDataFrame,
    .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] p,
    [data-testid="stChatMessageContent"] p,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
        color: {PRUSSIAN} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {PRUSSIAN};
    }}
    section[data-testid="stSidebar"] * {{
        color: {WHITE} !important;
    }}
    h1, h2, h3 {{
        color: {PRUSSIAN};
    }}
    .stButton>button {{
        background-color: {DENIM};
        color: {WHITE};
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.1rem;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: {PRUSSIAN};
        color: {WHITE};
    }}
    .mg-card {{
        background-color: {WHITE};
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        border-left: 6px solid {DENIM};
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }}
    .mg-badge {{
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        color: white;
        font-size: 0.78rem;
        font-weight: 600;
    }}
    .mg-chip {{
        display: inline-block;
        background-color: {ANAKIWA};
        color: {PRUSSIAN};
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        margin: 0.15rem 0.25rem 0.15rem 0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "text": "Hi Asha \U0001F44B I'm your MedGuardian copilot. Ask me anything about your medications."}
    ]
if "review_queue" not in st.session_state:
    hits = check_interactions(DEMO_PATIENT["medications"])
    st.session_state.review_queue = [
        {**h, "status": "Pending pharmacist review"} for h in hits if h["severity"] in ("moderate", "high")
    ]
if "patient_meds" not in st.session_state:
    st.session_state.patient_meds = list(DEMO_PATIENT["medications"])

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.markdown("## \U0001F48A MedGuardian AI")
st.sidebar.caption("AI-powered medication adherence & interaction copilot")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "\U0001F3E0  Patient Dashboard",
        "\U0001F4AC  AI Copilot",
        "\U0001F9D1\u200D\u2695\uFE0F  Pharmacist Review Queue",
        "\U0001FA7A  Physician View",
        "\U0001F4CA  KPI Dashboard",
        "\U0001F3ED  Pharma Program Insights",
        "\U0001F5C2\uFE0F  AI Project-Management Artifacts",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
if st.session_state.review_queue:
    pending = len([r for r in st.session_state.review_queue if r["status"] == "Pending pharmacist review"])
    st.sidebar.warning(f"{pending} alert(s) awaiting pharmacist review")
else:
    st.sidebar.success("No pending review items")

st.sidebar.caption(
    "Demo prototype \u2014 illustrative dataset only. Not for real clinical use."
)

# ---------------------------------------------------------------------------
# PAGE: Patient Dashboard
# ---------------------------------------------------------------------------
if page.startswith("\U0001F3E0"):
    st.title("Welcome back, Asha")
    st.caption(DEMO_PATIENT["condition_summary"])

    col1, col2, col3 = st.columns(3)
    log = generate_adherence_log()
    taken_pct = round(100 * sum(1 for d in log if d["taken"]) / len(log))
    with col1:
        st.markdown(
            f"""<div class="mg-card"><h4>Adherence (14 days)</h4>
            <h2 style="color:{DENIM}">{taken_pct}%</h2></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        n_meds = len(st.session_state.patient_meds)
        st.markdown(
            f"""<div class="mg-card"><h4>Active medications</h4>
            <h2 style="color:{DENIM}">{n_meds}</h2></div>""",
            unsafe_allow_html=True,
        )
    with col3:
        n_alerts = len(st.session_state.review_queue)
        st.markdown(
            f"""<div class="mg-card"><h4>Open interaction alerts</h4>
            <h2 style="color:{DENIM}">{n_alerts}</h2></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### Your medications")
    for m in st.session_state.patient_meds:
        info = MEDICATIONS_DB.get(m, {})
        st.markdown(
            f"""<div class="mg-card"><b>{m.title()}</b>
            <span class="mg-chip">{info.get('class','')}</span><br>
            <span style="color:#555">{info.get('common_use','')}</span></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### Add a new medication")
    new_med = st.selectbox("Select a medication to add", [""] + sorted(MEDICATIONS_DB.keys()))
    if st.button("Check & add"):
        if new_med:
            trial_list = st.session_state.patient_meds + [new_med]
            hits = [h for h in check_interactions(trial_list) if new_med in h["pair"]]
            if hits:
                for h in hits:
                    color = SEVERITY_COLOR[h["severity"]]
                    st.markdown(
                        f"""<div class="mg-card" style="border-left-color:{color}">
                        <span class="mg-badge" style="background-color:{color}">{h['severity'].upper()} RISK</span><br><br>
                        {h['explanation']}</div>""",
                        unsafe_allow_html=True,
                    )
                    if h["severity"] in ("moderate", "high"):
                        st.session_state.review_queue.append({**h, "status": "Pending pharmacist review"})
                st.info("This medication was added, and the flagged interaction was routed to your pharmacist for review.")
            else:
                st.success(f"No known interaction found for {new_med.title()}. Added to your list.")
            if new_med not in st.session_state.patient_meds:
                st.session_state.patient_meds.append(new_med)

    st.markdown("### 14-day adherence")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[d["date"] for d in log],
            y=[1 if d["taken"] else 0.3 for d in log],
            marker_color=[DENIM if d["taken"] else "#D9CFC8" for d in log],
            hovertext=["Taken" if d["taken"] else "Missed" for d in log],
        )
    )
    fig.update_layout(
        height=260, margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(visible=False), plot_bgcolor=WHITE, paper_bgcolor=WHITE,
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# PAGE: AI Copilot (this is where the client experiences the AI directly)
# ---------------------------------------------------------------------------
elif page.startswith("\U0001F4AC"):
    st.title("\U0001F4AC AI Copilot")
    st.caption(
        "Ask about interactions, a new medication, or staying on track. "
        "High and moderate-risk answers are always routed to a pharmacist before you see a recommendation to act on."
    )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="\U0001F48A" if msg["role"] == "assistant" else "\U0001F9D1"):
            st.markdown(msg["text"])

    user_msg = st.chat_input("e.g. Is it safe to take ibuprofen with my medications?")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "text": user_msg})
        with st.chat_message("user", avatar="\U0001F9D1"):
            st.markdown(user_msg)
        with st.chat_message("assistant", avatar="\U0001F48A"):
            with st.spinner("Checking your medications\u2026"):
                reply, source = get_copilot_reply(user_msg, st.session_state.patient_meds)
            st.markdown(reply)
            st.caption(f"Source: {'live LLM' if source == 'live-llm' else 'simulated AI (offline demo mode)'}")
        st.session_state.chat_history.append({"role": "assistant", "text": reply})

    st.markdown("---")
    if st.button("\U0001F9D1\u200D\u2695\uFE0F Talk to a pharmacist"):
        st.success("A pharmacist has been notified and will follow up within 2 hours (simulated).")

# ---------------------------------------------------------------------------
# PAGE: Pharmacist Review Queue (human-in-the-loop, per the MVP strategy)
# ---------------------------------------------------------------------------
elif page.startswith("\U0001F9D1"):
    st.title("\U0001F9D1\u200D\u2695\uFE0F Pharmacist Review Queue")
    st.caption("Every moderate/high-risk AI-flagged interaction is held here until a pharmacist actions it \u2014 the human-in-the-loop MVP design.")

    if not st.session_state.review_queue:
        st.success("Queue is empty.")
    for i, item in enumerate(st.session_state.review_queue):
        a, b = item["pair"]
        color = SEVERITY_COLOR[item["severity"]]
        with st.container():
            st.markdown(
                f"""<div class="mg-card" style="border-left-color:{color}">
                <span class="mg-badge" style="background-color:{color}">{item['severity'].upper()}</span>
                &nbsp;<b>{a.title()} + {b.title()}</b><br>
                <span style="color:#555">{item['explanation']}</span><br><br>
                <i>Status: {item['status']}</i></div>""",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            if item["status"] == "Pending pharmacist review":
                if c1.button("Approve alert to patient", key=f"approve_{i}"):
                    st.session_state.review_queue[i]["status"] = "Approved \u2014 sent to patient"
                    st.rerun()
                if c2.button("Dismiss (false positive)", key=f"dismiss_{i}"):
                    st.session_state.review_queue[i]["status"] = "Dismissed by pharmacist"
                    st.rerun()

# ---------------------------------------------------------------------------
# PAGE: Physician View (Specialty Pharma Extension — closes the loop with the
# prescriber, not just the pharmacist; see Section 13 of the product proposal)
# ---------------------------------------------------------------------------
elif page.startswith("\U0001FA7A"):
    st.title("\U0001FA7A Physician View")
    st.caption(
        f"{SPECIALTY_PROGRAM['program_name']} — {SPECIALTY_PROGRAM['indication']}. "
        "Extends the human-in-the-loop design to the prescriber: a physician sees adherence "
        "and interaction trends for their own patients, not just a downstream pharmacist queue."
    )
    st.info(
        f"Illustrative panel only. Shown with patient consent as part of {SPECIALTY_PROGRAM['drug_name']} "
        "specialty care support."
    )

    for p in PHYSICIAN_PANEL:
        status_color = {"Stable": SEVERITY_COLOR["low"], "Watch": SEVERITY_COLOR["moderate"], "At risk": SEVERITY_COLOR["high"]}[p["status"]]
        st.markdown(
            f"""<div class="mg-card" style="border-left-color:{status_color}">
            <b>{p['name']}</b>
            <span class="mg-badge" style="background-color:{status_color}">{p['status'].upper()}</span><br>
            <span style="color:#555">{p['med']}</span><br>
            Adherence: <b>{p['adherence_pct']}%</b> &nbsp;|&nbsp; Last flag: {p['last_flag']}</div>""",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# PAGE: KPI Dashboard
# ---------------------------------------------------------------------------
elif page.startswith("\U0001F4CA"):
    st.title("\U0001F4CA KPI Dashboard")
    st.caption("Live view of the Metrics Framework defined in the product proposal.")

    cols = st.columns(len(KPI_SNAPSHOT))
    for col, (name, kpi) in zip(cols, KPI_SNAPSHOT.items()):
        color = STATUS_COLOR[kpi["status"]]
        col.markdown(
            f"""<div class="mg-card" style="border-left-color:{color}">
            <span style="font-size:0.85rem;color:#555">{name}</span><br>
            <h2 style="color:{PRUSSIAN};margin:0.1rem 0">{kpi['value']}</h2>
            <span style="font-size:0.78rem;color:#777">Threshold: {kpi['threshold']}</span></div>""",
            unsafe_allow_html=True,
        )

    df = pd.DataFrame(
        {
            "KPI": list(KPI_SNAPSHOT.keys()),
            "Status": [k["status"].replace("_", " ").title() for k in KPI_SNAPSHOT.values()],
        }
    )
    st.markdown("### Status summary")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# PAGE: Pharma Program Insights (Specialty Pharma Extension — de-identified,
# aggregate view for a pharma manufacturer's patient support program team;
# closes the loop described in Section 13 of the product proposal)
# ---------------------------------------------------------------------------
elif page.startswith("\U0001F3ED"):
    st.title("\U0001F3ED Pharma Program Insights")
    st.caption(f"{SPECIALTY_PROGRAM['program_name']} — de-identified, consented, aggregate data only. No individual patient is ever visible here.")

    cols = st.columns(3)
    stats = [
        ("Enrolled patients", PHARMA_INSIGHTS["enrolled_patients"]),
        ("Average adherence", PHARMA_INSIGHTS["avg_adherence_rate"]),
        ("Flagged high discontinuation risk", PHARMA_INSIGHTS["discontinuation_risk_high"]),
    ]
    for col, (label, value) in zip(cols, stats):
        col.markdown(
            f"""<div class="mg-card"><h4>{label}</h4>
            <h2 style="color:{DENIM}">{value}</h2></div>""",
            unsafe_allow_html=True,
        )

    cols2 = st.columns(3)
    stats2 = [
        ("Interaction flags resolved (90d)", PHARMA_INSIGHTS["interaction_flags_resolved_90d"]),
        ("Pharmacist escalations (90d)", PHARMA_INSIGHTS["pharmacist_escalations_90d"]),
        ("Est. doses preserved (90d)", PHARMA_INSIGHTS["est_doses_saved_90d"]),
    ]
    for col, (label, value) in zip(cols2, stats2):
        col.markdown(
            f"""<div class="mg-card"><h4>{label}</h4>
            <h2 style="color:{DENIM}">{value}</h2></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### Adherence trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[t["month"] for t in PHARMA_ADHERENCE_TREND],
        y=[t["adherence_pct"] for t in PHARMA_ADHERENCE_TREND],
        mode="lines+markers", line=dict(color=DENIM, width=3), marker=dict(size=8, color=DENIM),
    ))
    fig.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(title="Adherence %", range=[60, 100]), plot_bgcolor=WHITE, paper_bgcolor=WHITE,
    )
    st.plotly_chart(fig, use_container_width=True)

    if st.button("\U0001F916 Generate AI program summary for medical affairs"):
        with st.spinner("Summarizing program data…"):
            summary, source = generate_pharma_insights_summary(PHARMA_INSIGHTS, PHARMA_ADHERENCE_TREND)
        st.markdown(f'<div class="mg-card">{summary}</div>', unsafe_allow_html=True)
        st.caption(f"Source: {'live LLM' if source == 'live-llm' else 'simulated AI (offline demo mode)'}")

# ---------------------------------------------------------------------------
# PAGE: AI for Project-Management Artifacts
# ---------------------------------------------------------------------------
elif page.startswith("\U0001F5C2"):
    st.title("\U0001F5C2\uFE0F AI for Project-Management Artifacts")
    st.caption(
        "The AI layer isn't only patient-facing \u2014 it also keeps the product team's own "
        "roadmap, risk register, and backlog summarized and stakeholder-ready on demand."
    )

    tab1, tab2, tab3 = st.tabs(["Roadmap", "Risk Register", "Backlog"])

    with tab1:
        df = pd.DataFrame(ROADMAP)
        st.dataframe(df, use_container_width=True, hide_index=True)
        if st.button("\U0001F916 Generate AI roadmap status update"):
            with st.spinner("Summarizing roadmap\u2026"):
                summary, source = generate_pm_summary("roadmap", ROADMAP)
            st.markdown(f'<div class="mg-card">{summary}</div>', unsafe_allow_html=True)
            st.caption(f"Source: {'live LLM' if source == 'live-llm' else 'simulated AI (offline demo mode)'}")

    with tab2:
        df = pd.DataFrame(RISK_REGISTER)
        st.dataframe(df, use_container_width=True, hide_index=True)
        if st.button("\U0001F916 Generate AI risk summary"):
            with st.spinner("Summarizing risk register\u2026"):
                summary, source = generate_pm_summary("risk", RISK_REGISTER)
            st.markdown(f'<div class="mg-card">{summary}</div>', unsafe_allow_html=True)
            st.caption(f"Source: {'live LLM' if source == 'live-llm' else 'simulated AI (offline demo mode)'}")

    with tab3:
        df = pd.DataFrame(BACKLOG)
        st.dataframe(df, use_container_width=True, hide_index=True)
        if st.button("\U0001F916 Generate AI backlog summary"):
            with st.spinner("Summarizing backlog\u2026"):
                summary, source = generate_pm_summary("backlog", BACKLOG)
            st.markdown(f'<div class="mg-card">{summary}</div>', unsafe_allow_html=True)
            st.caption(f"Source: {'live LLM' if source == 'live-llm' else 'simulated AI (offline demo mode)'}")

    st.info(
        "In production, set the ANTHROPIC_API_KEY environment variable to have these "
        "summaries generated by a real Claude model instead of the offline simulated fallback \u2014 "
        "see README.md."
    )
