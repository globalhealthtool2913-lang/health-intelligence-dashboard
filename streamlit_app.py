import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from sklearn.linear_model import LinearRegression
import random

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="WHO Predictive Intelligence v2",
    layout="wide"
)

st_autorefresh(interval=15000, key="refresh")

# -----------------------------
# TITLE
# -----------------------------
st.title("🌍 WHO GLOBAL PREDICTIVE HEALTH INTELLIGENCE SYSTEM (v2)")
st.caption("AI + Predictive Outbreak Surveillance Engine")

# -----------------------------
# COUNTRIES
# -----------------------------
countries = [
    "Ethiopia", "Kenya", "Sudan", "Uganda", "Nigeria",
    "India", "Brazil", "Germany", "USA", "China"
]

# -----------------------------
# SESSION MEMORY (CRITICAL FOR PREDICTION)
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = {c: [] for c in countries}

# -----------------------------
# GENERATE SIGNALS
# -----------------------------
records = []

for country in countries:

    epi = random.randint(20, 100)
    health = random.randint(20, 100)
    social = random.randint(20, 100)
    media = random.randint(20, 100)

    risk = (
        epi * 0.4 +
        health * 0.25 +
        social * 0.2 +
        media * 0.15
    )

    # Save history
    st.session_state.history[country].append(risk)

    if len(st.session_state.history[country]) > 10:
        st.session_state.history[country].pop(0)

    records.append({
        "Country": country,
        "Epidemiology": epi,
        "Healthcare": health,
        "Social": social,
        "Media": media,
        "Risk Score": round(risk, 2)
    })

df = pd.DataFrame(records)

# -----------------------------
# PREDICTION ENGINE (REAL MODEL)
# -----------------------------
def predict_future(series):
    if len(series) < 3:
        return series[-1]

    X = np.array(range(len(series))).reshape(-1, 1)
    y = np.array(series)

    model = LinearRegression()
    model.fit(X, y)

    return float(model.predict([[len(series) + 1]])[0])

df["Predicted Risk"] = df["Country"].apply(
    lambda c: predict_future(st.session_state.history[c])
)

# -----------------------------
# RISK CLASSIFICATION
# -----------------------------
def classify(score):
    if score >= 80:
        return "🔴 Critical"
    elif score >= 65:
        return "🟠 High"
    elif score >= 45:
        return "🟡 Moderate"
    return "🟢 Low"

df["Risk Level"] = df["Risk Score"].apply(classify)

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("High Risk Zones", len(df[df["Risk Score"] > 70]))
col3.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col4.metric("AI Engine", "PREDICTIVE MODE")

# -----------------------------
# ALERTS
# -----------------------------
st.subheader("🚨 Active WHO Alerts")

alerts = df[df["Risk Score"] >
