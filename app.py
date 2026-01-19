import streamlit as st
from src.config import DATA_PATHS, DEFAULT_Z_THRESHOLD
from src.data_loader import lazy_load
from src.preprocessing import *
from src.lifecycle import build_lifecycle
from src.anomaly import detect_anomalies
from src.risk_scoring import compute_risk_score
from src.exec_summary import render_executive_summary
from src.lifecycle_overview import render_lifecycle_overview
from src.anomaly_intelligence import render_anomaly_intelligence
from src.equity_view import render_equity_view
from src.methodology import render_methodology

st.set_page_config(page_title="Aadhaar Lifecycle Analytics", layout="wide")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Summary",
        "Lifecycle Overview",
        "Anomaly Intelligence",
        "Equity & Inclusion",
        "Methodology"
    ]
)

@st.cache_data
def pipeline(z):
    enroll = preprocess_enrollment(lazy_load(DATA_PATHS["enrolment"]))
    bio = preprocess_biometric(lazy_load(DATA_PATHS["biometric"]))
    demo = preprocess_demographic(lazy_load(DATA_PATHS["demographic"]))

    df = build_lifecycle(enroll, bio, demo)
    df = detect_anomalies(df, z)
    return compute_risk_score(df)

data = pipeline(DEFAULT_Z_THRESHOLD)

if page == "Executive Summary":
    render_executive_summary(data)
elif page == "Lifecycle Overview":
    render_lifecycle_overview(data)
elif page == "Anomaly Intelligence":
    render_anomaly_intelligence(data)
elif page == "Equity & Inclusion":
    render_equity_view(data)
else:
    render_methodology()
