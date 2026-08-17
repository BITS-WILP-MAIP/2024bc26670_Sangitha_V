"""Patient Dashboard — medication list, barcode/photo capture, daily check-in."""

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.adherence import daily_adherence_pct, overall_adherence_pct
from src.ai_layer import is_live, summarize_interaction_text
from src.config import resolve_data_path
from src.drug_normalizer import CANONICAL_DRUGS, load_orange_book_ingredients, normalize_to_canonical
from src.fda_reference import get_reference_text, load_fda_reference_text
from src.interaction_engine import check_interactions, load_interactions
from src.state import build_patient_state

from .theme import SEVERITY_COLOR

ROLE_COLOR_PALETTE = ["#0A53BE", "#94BFE7", "#A8D5FF", "#D98A0D", "#3E8E5B", "#C0392B", "#7A5EA8"]


@st.cache_data(show_spinner=False)
def _cached_ingredients(path_str):
    return load_orange_book_ingredients(path_str)


@st.cache_data(show_spinner=False)
def _cached_interactions(path_str):
    return load_interactions(path_str)


@st.cache_data(show_spinner=False)
def _cached_fda_reference(path_str):
    return load_fda_reference_text(path_str)


@st.cache_data(show_spinner="Summarizing the FDA label text…")
def _cached_summary(raw_text):
    return summarize_interaction_text(raw_text)


def _show_fda_reference(ob_name, fda_reference_map):
    """Surface real, FDA-sourced label text when our small pairwise table
    has nothing — real reference context instead of nothing, with the
    source label always shown so a combination-product attribution can't
    be misread as a single-ingredient monograph. The raw label text is
    dense regulatory prose, so it's summarized into a short table before
    display — live by Claude when ANTHROPIC_API_KEY is set (a Phase 2
    preview capability), or a deterministic reformat otherwise."""
    ref = get_reference_text(ob_name, fda_reference_map)
    if not ref:
        return
    with st.expander("📋 FDA label reference — Drug Interactions (summarized)"):
        st.caption(f"Source label: {ref['source_brand']} (openFDA) — may be a combination product; read attribution carefully.")
        rows, source = _cached_summary(ref["text"])
        if source in ("live-llm", "simulated-table") and rows:
            st.dataframe(
                pd.DataFrame(rows, columns=["Interacts with", "What can happen", "What to do"]),
                use_container_width=True, hide_index=True,
            )
        elif rows:
            for bullet in rows:
                st.markdown(f"- {bullet}")
        else:
            st.write(ref["text"])
        if source == "live-llm":
            st.caption("✨ Summarized live by Claude — a Phase 2 preview capability, not part of the Phase 1 zero-AI pilot scope.")
        else:
            st.caption(
                "⚙️ Deterministic, rule-based reformat — no live AI call was made "
                f"({'ANTHROPIC_API_KEY not set for this session' if not is_live() else 'the live call did not return a usable result'})."
            )
        if st.checkbox("Show full raw FDA label text", key=f"raw_{ob_name}"):
            st.write(ref["text"])


def _add_medication(ob_name, interactions, fda_reference_map, theme):
    """Shared confirm-and-check logic for both capture methods."""
    canon = normalize_to_canonical(ob_name)
    if canon is None:
        st.warning(
            f"**{ob_name}** isn't in this pilot's reference interaction set yet. "
            "Per the risk mitigation in Section 9 of the product proposal, an unmatched "
            "medication is never silently ignored — it's routed to your pharmacist for manual review."
        )
        _show_fda_reference(ob_name, fda_reference_map)
        st.session_state.review_queue.append({
            "pair": (ob_name, "(unmatched)"), "severity": "moderate",
            "explanation": f"Medication '{ob_name}' has no reference interaction data in this pilot's dataset — needs manual pharmacist review before use is confirmed safe.",
            "status": "Pending pharmacist review",
        })
        st.session_state.patient_meds.append(ob_name.upper())
        return

    trial_list = st.session_state.patient_meds + [canon]
    hits = [h for h in check_interactions(trial_list, interactions) if canon in h["pair"]]
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
        st.info(f"Matched to **{canon.title()}**. Added, and the flagged interaction was routed to your pharmacist for review.")
    else:
        st.success(f"Matched to **{canon.title()}**. No known interaction found in our small reference table — added to your list.")
        _show_fda_reference(canon, fda_reference_map)
    if canon not in st.session_state.patient_meds:
        st.session_state.patient_meds.append(canon)


def _remove_medication(drug_name):
    """Drop a medication and any pending interaction alerts that reference
    it — once it's no longer being taken, an alert about it no longer
    applies. Historical adherence log entries are left untouched."""
    st.session_state.patient_meds = [m for m in st.session_state.patient_meds if m != drug_name]
    st.session_state.review_queue = [r for r in st.session_state.review_queue if drug_name not in r["pair"]]


def render_patient_dashboard(config):
    theme = config["theme"]
    demo_patient_name = "Asha"
    ingredients = _cached_ingredients(str(resolve_data_path(config, "orange_book_drugs")))
    interactions = _cached_interactions(str(resolve_data_path(config, "orange_book_interactions")))
    fda_reference_map = _cached_fda_reference(str(resolve_data_path(config, "fda_reference_text")))

    st.title(f"Welcome back, {demo_patient_name}")
    st.caption(config["condition"]["name"])

    log = st.session_state.adherence_log
    taken_pct = overall_adherence_pct(log)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="mg-card"><h4>Adherence (14 days)</h4>
            <h2 style="color:{theme['denim']}">{taken_pct}%</h2></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="mg-card"><h4>Active medications</h4>
            <h2 style="color:{theme['denim']}">{len(st.session_state.patient_meds)}</h2></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="mg-card"><h4>Open interaction alerts</h4>
            <h2 style="color:{theme['denim']}">{len(st.session_state.review_queue)}</h2></div>""", unsafe_allow_html=True)

    col_heading, col_reset = st.columns([5, 2])
    with col_heading:
        st.markdown("### Your medications")
    with col_reset:
        if st.button("🔄 Reset to demo defaults", key="reset_meds"):
            for key, value in build_patient_state(config, interactions).items():
                st.session_state[key] = value
            st.rerun()

    if not st.session_state.patient_meds:
        st.info("No medications yet — add one below.")

    for m in st.session_state.patient_meds:
        info = CANONICAL_DRUGS.get(m, {})
        col_card, col_remove = st.columns([6, 1])
        with col_card:
            st.markdown(
                f"""<div class="mg-card"><b>{m.title()}</b>
                <span class="mg-chip">{info.get('class', 'Reference data not yet available')}</span><br>
                <span style="color:#555">{info.get('common_use', '')}</span></div>""",
                unsafe_allow_html=True,
            )
            _show_fda_reference(m, fda_reference_map)
        with col_remove:
            st.write("")
            if st.button("✕ Remove", key=f"remove_{m}"):
                _remove_medication(m)
                st.rerun()

    st.markdown("### Current regimen — combination therapy view")
    st.caption(
        "Illustrative grouping of your active medications by role in the regimen — "
        "reference only, not clinical guidance (Phase 1 pilot scope, Section 11)."
    )
    if st.session_state.patient_meds:
        rows = [
            {
                "Medication": m.title(),
                "Class": CANONICAL_DRUGS.get(m, {}).get("class", "Unclassified"),
                "Role in regimen": CANONICAL_DRUGS.get(m, {}).get("regimen_role", "Unclassified"),
            }
            for m in st.session_state.patient_meds
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        roles = sorted({r["Role in regimen"] for r in rows})
        role_colors = {role: ROLE_COLOR_PALETTE[i % len(ROLE_COLOR_PALETTE)] for i, role in enumerate(roles)}
        fig_regimen = go.Figure()
        for role in roles:
            meds_in_role = [r["Medication"] for r in rows if r["Role in regimen"] == role]
            fig_regimen.add_trace(go.Bar(
                y=["Current combination"] * len(meds_in_role),
                x=[1] * len(meds_in_role),
                name=role,
                orientation="h",
                marker_color=role_colors[role],
                text=meds_in_role,
                textposition="inside",
                hovertext=meds_in_role,
            ))
        fig_regimen.update_layout(
            barmode="stack", height=170, margin=dict(l=10, r=10, t=30, b=30),
            xaxis_title=f"{len(rows)} medication(s) in current combination",
            yaxis_title="",
            xaxis=dict(showticklabels=False),
            legend_title_text="Role in regimen",
            plot_bgcolor=theme["white"], paper_bgcolor=theme["white"],
        )
        st.plotly_chart(fig_regimen, use_container_width=True)
    else:
        st.info("No active medications — add one below to see the regimen view.")

    st.markdown("### Add a new medication")
    st.caption("Barcode/photo capture, auto-matched against a real FDA drug reference list — not manual free-text entry (UX spec 5.1).")
    tab1, tab2 = st.tabs(["\U0001F4F7 Scan label or bottle", "\U0001F50D Search manually"])

    with tab1:
        uploaded = st.file_uploader("Take a photo of your prescription label or pill bottle", type=["png", "jpg", "jpeg"])
        st.caption("Simulated OCR match for this demo — a production build auto-matches via an RxNorm-backed imaging API.")
        if uploaded is not None:
            with st.spinner("Reading label…"):
                pass
            photo_match = st.selectbox(
                "We detected this medication — confirm the match:",
                [""] + ingredients,
                key="photo_match",
            )
            if st.button("Confirm & check", key="confirm_photo") and photo_match:
                _add_medication(photo_match, interactions, fda_reference_map, theme)

    with tab2:
        manual_match = st.selectbox("Search the FDA drug reference list", [""] + ingredients, key="manual_match")
        if st.button("Check & add", key="confirm_manual") and manual_match:
            _add_medication(manual_match, interactions, fda_reference_map, theme)

    st.markdown("### Today's check-in")
    today_iso = datetime.now().date().isoformat()
    if st.session_state.today_logged:
        st.success("Today is logged. Thanks for checking in!")
        todays = st.session_state.adherence_log.get(today_iso, {})
        taken_list = [m.title() for m, v in todays.items() if v]
        missed_list = [m.title() for m, v in todays.items() if not v]
        if taken_list:
            st.caption(f"✅ Taken: {', '.join(taken_list)}")
        if missed_list:
            st.caption(f"❌ Skipped: {', '.join(missed_list)}")
    elif not st.session_state.patient_meds:
        st.info("Add a medication above to log today's check-in.")
    else:
        st.caption("Which medications did you take today?")
        num_cols = min(3, len(st.session_state.patient_meds))
        cols = st.columns(num_cols)
        taken_selection = {}
        for idx, m in enumerate(st.session_state.patient_meds):
            with cols[idx % num_cols]:
                taken_selection[m] = st.checkbox(m.title(), value=True, key=f"checkin_{m}")
        c1, c2 = st.columns(2)
        if c1.button("✅ Save today's check-in"):
            st.session_state.adherence_log[today_iso] = taken_selection
            st.session_state.today_logged = True
            st.rerun()
        if c2.button("⏰ Remind me later"):
            st.info("We'll remind you again in a few hours (simulated).")

    st.markdown("### 14-day adherence")
    history = daily_adherence_pct(st.session_state.adherence_log)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[d for d, _ in history],
        y=[pct for _, pct in history],
        marker_color=[theme["denim"] if pct >= 80 else "#D9CFC8" for _, pct in history],
        hovertext=[f"{pct}% of medications taken" for _, pct in history],
        name="Adherence",
    ))
    fig.update_layout(
        height=280, margin=dict(l=10, r=10, t=30, b=40),
        xaxis_title="Date", yaxis_title="Adherence (% of medications taken)",
        yaxis=dict(range=[0, 100]),
        showlegend=False,
        plot_bgcolor=theme["white"], paper_bgcolor=theme["white"],
    )
    st.plotly_chart(fig, use_container_width=True)
