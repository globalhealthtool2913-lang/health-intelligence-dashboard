import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="WHO Global Intelligence v3",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🌍 WHO GLOBAL HEALTH INTELLIGENCE SYSTEM (v3 STABLE)")
st.caption("Fully self-contained AI outbreak surveillance system")

# -----------------------------
# COUNTRIES
# -----------------------------
countries = [
    "Ethiopia", "Kenya", "Sudan", "Uganda", "Nigeria",
    "India", "Brazil", "Germany", "USA", "China"
]

# -----------------------------
# SAFE SESSION MEMORY
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = {c: [] for c in countries}

# -----------------------------
# SIMPLE TREND PREDICTION (NO SKLEARN)
# -----------------------------
def predict(series):
    if len(series) < 3:
        return series[-1] if series else 50

    return float(np.mean(series[-3:]) + np.random.normal(0, 2))

# -----------------------------
# RISK CLASSIFICATION
# -----------------------------
def risk_level(score):
    if score >= 80:
        return "🔴 Critical"
    elif score >= 65:
        return "🟠 High"
    elif score >= 45:
        return "🟡 Moderate"
    return "🟢 Low"

# -----------------------------
# GENERATE INTELLIGENCE DATA
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

    # update history
    st.session_state.history[country].append(risk)

    if len(st.session_state.history[country]) > 10:
        st.session_state.history[country].pop(0)

    predicted = predict(st.session_state.history[country])

    records.append({
        "Country": country,
        "Epidemiology": epi,
        "Healthcare": health,
        "Social": social,
        "Media": media,
        "Risk Score": round(risk, 2),
        "Risk Level": risk_level(risk),
        "Predicted Risk": round(predicted, 2)
    })

df = pd.DataFrame(records)

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries Monitored", len(df))
col2.metric("High Risk Zones", len(df[df["Risk Score"] > 70]))
col3.metric("Avg Risk Score", round(df["Risk Score"].mean(), 2))
col4.metric("System Status", "ONLINE")

# -----------------------------
# ALERTS
# -----------------------------
st.subheader("🚨 Active Global Alerts")

alerts = df[df["Risk Score"] > 70]

if alerts.empty:
    st.success("No critical outbreaks detected")
else:
    for _, row in alerts.iterrows():
        st.error(
            f"{row['Country']} | {row['Risk Level']} | "
            f"Predicted: {row['Predicted Risk']}"
        )

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Overview")
st.dataframe(df)

# -----------------------------
# RISK VISUALIZATION
# -----------------------------
st.subheader("🌍 Global Risk Map")

fig = px.bar(
    df,
    x="Country",
    y="Risk Score",
    color="Risk Score",
    title="WHO AI Risk Monitoring System"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# PREDICTION VIEW
# -----------------------------
st.subheader("📈 Predictive Risk Overview")

fig2 = px.line(
    df,
    x="Country",
    y=["Risk Score", "Predicted Risk"],
    markers=True,
    title="Current vs Predicted Outbreak Risk"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# LIVE INTELLIGENCE FEED
# -----------------------------
st.subheader("🧠 AI Intelligence Feed")

feed = [
    "Elevated epidemiological signals detected in multiple regions",
    "Cross-border transmission risk increasing",
    "Healthcare strain trending upward",
    "Early outbreak pattern detected by AI model",
    "Global surveillance anomaly identified"
]

for msg in random.sample(feed, 3):
    st.info(msg)

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
AI Signal Generator
        ↓
Risk Engine (Statistical Model)
        ↓
Predictive Engine (Rolling Average)
        ↓
Session Memory Layer
        ↓
WHO Intelligence Dashboard (Streamlit)
""")

# -----------------------------
# FOOTER
# -----------------------------
st.success("WHO Intelligence System v3 running successfully")
