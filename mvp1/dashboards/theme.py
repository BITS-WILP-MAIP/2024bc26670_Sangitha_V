"""Sandoz blue theme — shared CSS injection for every dashboard page."""

import streamlit as st

SEVERITY_COLOR = {"low": "#3E8E5B", "moderate": "#D98A0D", "high": "#C0392B"}
STATUS_COLOR = {"on_track": "#3E8E5B", "at_risk": "#D98A0D", "off_track": "#C0392B"}


def apply_theme(t):
    """t: config['theme'] dict (denim, prussian, cornflower, anakiwa, pampas, white)."""
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {t['pampas']}; color: {t['prussian']}; }}
        .stApp p, .stApp li, .stApp span, .stApp label, .stApp div,
        .stMarkdown, .stMarkdown p, [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p, .stDataFrame,
        .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] p,
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {t['prussian']} !important;
        }}
        section[data-testid="stSidebar"] {{ background-color: {t['prussian']}; }}
        section[data-testid="stSidebar"] * {{ color: {t['white']} !important; }}
        h1, h2, h3 {{ color: {t['prussian']}; }}
        .stButton>button {{
            background-color: {t['denim']}; color: {t['white']}; border-radius: 8px;
            border: none; padding: 0.5rem 1.1rem; font-weight: 600;
        }}
        .stButton>button:hover {{ background-color: {t['prussian']}; color: {t['white']}; }}
        .mg-card {{
            background-color: {t['white']}; border-radius: 12px; padding: 1.1rem 1.3rem;
            margin-bottom: 0.9rem; border-left: 6px solid {t['denim']};
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }}
        .mg-badge {{
            display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px;
            color: white; font-size: 0.78rem; font-weight: 600;
        }}
        .mg-chip {{
            display: inline-block; background-color: {t['anakiwa']}; color: {t['prussian']};
            padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.8rem;
            margin: 0.15rem 0.25rem 0.15rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
