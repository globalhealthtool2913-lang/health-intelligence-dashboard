   import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

from sklearn.ensemble import RandomForestRegressor

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="WHO AI Outbreak Intelligence System",
    layout="wide"
)

st.title("🌍 WHO AI Outbreak Intelligence System")
st.caption("AI + Time-Series Epidemiology Monitoring Dashboard")

# =============================
# COUNTRIES
# =============================
countries = [
    "Ethiopia", "Kenya", "Sudan", "Uganda", "Nigeria",
    "India", "Brazil", "Germany", "USA", "China"
]

# =============================
# MEMORY SYSTEM (TIME SERIES)
# =============================
if "history" not in st.session_state:
    st.session_state.history = {c: [] for c in countries}

# =============================
# DATA GENERATION + MEMORY
# =============================
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

    # -------------------------
    # STORE TIME-SERIES MEMORY
    # -------------------------
    st.session_state.history[c].append(risk)

    if len(st.session_state.history[c]) > 10:
        st.session_state.history[c].pop(0)

    data.append({
        "Country": c,
        "Epidemiology": epi,
        "Healthcare": health,
        "Social": social,
        "Media": media,
        "Risk Score": risk
    })

df = pd.DataFrame(data)

# =============================
# AI MODEL
# =============================
model = RandomForestRegressor(n_estimators=150, random_state=42)

X = df[["Epidemiology", "Healthcare", "Social", "Media"]]
y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# =============================
# RISK LEVEL
# =============================
def risk_level(x):
    if x > 80:
        return "High"
    elif x > 60:
        return "Moderate"
    return "Low"

df["Risk Level"] = df["AI Prediction"].apply(risk_level)

# =============================
# METRICS
# =============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("High Risk", len(df[df["AI Prediction"] > 80]))
col3.metric("Avg Risk", round(df["AI Prediction"].mean(), 2))
col4.metric("System", "ACTIVE")

# =============================
# ALERT SYSTEM
# =============================
st.subheader("🚨 Alerts")

alerts = df[df["AI Prediction"] > 80]

if alerts.empty:
    st.success("No high-risk outbreak signals detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} | Risk: {row['Risk Level']}")

# =============================
# TABLE
# =============================
st.subheader("📊 Data Overview")
st.dataframe(df)

# =============================
# VISUALIZATION 1
# =============================
st.subheader("🌍 Global Risk Distribution")

fig = px.bar(
    df,
    x="Country",
    y="AI Prediction",
    color="AI Prediction",
    title="AI Risk Across Countries"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# VISUALIZATION 2
# =============================
st.subheader("📈 AI vs Risk Score")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="AI Prediction",
    title="Prediction Correlation View"
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# 🧠 TIME-SERIES MEMORY VIEW
# =============================
st.subheader("📈 Outbreak Time-Series Memory")

selected_country = st.selectbox("Select Country", countries)

history = st.session_state.history.get(selected_country, [])

if len(history) > 1:

    ts_df = pd.DataFrame({
        "Time Step": list(range(len(history))),
        "Risk": history
    })

    fig3 = px.line(
        ts_df,
        x="Time Step",
        y="Risk",
        title=f"{selected_country} Risk Evolution"
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Not enough history yet — keep running the app")

# =============================
# SYSTEM FEED
# =============================
st.subheader("🧠 System Feed")

messages = [
    "Monitoring epidemiological signals...",
    "Updating AI risk models...",
    "Tracking global health patterns...",
    "Processing multi-region data streams...",
    "System operating normally..."
]

for msg in random.sample(messages, 3):
    st.info(msg)

# =============================
# FOOTER
# =============================
st.success("System running with Time-Series Memory Enabled") 
