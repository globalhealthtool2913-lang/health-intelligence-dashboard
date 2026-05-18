import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="WHO AI Outbreak System",
    layout="wide"
)

# -----------------------------
# TITLE (CLEAN)
# -----------------------------
st.title("🌍 WHO AI Outbreak Intelligence System")
st.caption("Experimental AI-based global health monitoring dashboard")

# -----------------------------
# COUNTRIES
# -----------------------------
countries = [
    "Ethiopia", "Kenya", "Sudan", "Uganda", "Nigeria",
    "India", "Brazil", "Germany", "USA", "China"
]

# -----------------------------
# DATA GENERATION
# -----------------------------
data = []

for c in countries:

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

    data.append({
        "Country": c,
        "Epidemiology": epi,
        "Healthcare": health,
        "Social": social,
        "Media": media,
        "Risk Score": risk
    })

df = pd.DataFrame(data)

# -----------------------------
# ML MODEL
# -----------------------------
model = RandomForestRegressor(n_estimators=150, random_state=42)

X = df[["Epidemiology", "Healthcare", "Social", "Media"]]
y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# -----------------------------
# RISK LEVELS
# -----------------------------
def risk_level(x):
    if x > 80:
        return "High"
    elif x > 60:
        return "Moderate"
    return "Low"

df["Risk Level"] = df["AI Prediction"].apply(risk_level)

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("High Risk", len(df[df["AI Prediction"] > 80]))
col3.metric("Avg Risk", round(df["AI Prediction"].mean(), 2))
col4.metric("System", "Active")

# -----------------------------
# ALERTS
# -----------------------------
st.subheader("🚨 Alerts")

alerts = df[df["AI Prediction"] > 80]

if alerts.empty:
    st.success("No high-risk signals detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} - Risk: {row['Risk Level']}")

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Data Overview")
st.dataframe(df)

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("🌍 Risk Visualization")

fig = px.bar(
    df,
    x="Country",
    y="AI Prediction",
    color="AI Prediction",
    title="Global Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# COMPARISON CHART
# -----------------------------
st.subheader("📈 Comparison View")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="AI Prediction",
    title="Risk vs AI Prediction"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# FEED
# -----------------------------
st.subheader("🧠 System Feed")

messages = [
    "Monitoring global health signals...",
    "Updating risk indicators...",
    "Analyzing epidemiological patterns...",
    "Processing multi-region data...",
    "System running normally..."
]

for msg in random.sample(messages, 3):
    st.info(msg)

# -----------------------------
# FOOTER
# -----------------------------
st.success("System running successfully")
    
