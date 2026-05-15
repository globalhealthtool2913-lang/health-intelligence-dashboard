import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="RW-10 Global Health Intelligence", layout="wide")

st.title("🌍 Global Health Intelligence Platform (RW-10)")
st.caption("Operational outbreak intelligence system with trends, sources, and exports")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

risk_filter = st.sidebar.multiselect(
    "Filter Risk Level",
    ["HIGH", "MODERATE", "LOW"],
    default=["HIGH", "MODERATE", "LOW"]
)

source_filter = st.sidebar.multiselect(
    "Filter Source",
    ["WHO", "Africa CDC", "UNICEF", "ReliefWeb"],
    default=["WHO", "Africa CDC", "UNICEF", "ReliefWeb"]
)

# -----------------------------
# DATA (SIMULATED REAL-WORLD STRUCTURE)
# -----------------------------
data = [
    {
        "event": "Cholera outbreak reported",
        "country": "Ethiopia",
        "source": "WHO",
        "date": "2026-05-15"
    },
    {
        "event": "Flooding affecting hospitals",
        "country": "Kenya",
        "source": "ReliefWeb",
        "date": "2026-05-14"
    },
    {
        "event": "Conflict limiting healthcare access",
        "country": "Sudan",
        "source": "UNICEF",
        "date": "2026-05-13"
    },
    {
        "event": "Malaria surge detected",
        "country": "Somalia",
        "source": "Africa CDC",
        "date": "2026-05-12"
    },
    {
        "event": "Food insecurity crisis escalating",
        "country": "South Sudan",
        "source": "WHO",
        "date": "2026-05-11"
    }
]

df = pd.DataFrame(data)

# -----------------------------
# FILTER DATA
# -----------------------------
df = df[df["country"] == country]
df = df[df["source"].isin(source_filter)]

# -----------------------------
#
