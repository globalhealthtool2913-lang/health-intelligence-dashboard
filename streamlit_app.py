import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from datetime import datetime
import random
import sqlite3

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="WHO Global Health Intelligence System",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🏥 WHO GLOBAL HEALTH INTELLIGENCE SYSTEM")
st.caption("AI-Powered Surveillance & Outbreak Prediction Platform")

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("who_health.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS intelligence (
    country TEXT,
    risk REAL,
    outbreak INTEGER,
    timestamp TEXT
)
""")

conn.commit()

# -----------------------------
# COUNTRIES
# -----------------------------
countries = [
    "Ethiopia",
    "Kenya",
    "Sudan",
    "Uganda",
    "Nigeria",
    "India",
    "Brazil",
    "Germany",
    "USA",
    "China"
]

# -----------------------------
# AI SIGNAL GENERATION
# -----------------------------
data = []

for country in countries:
    epidemiology = random.randint(20, 100)
    healthcare = random.randint(20, 100)
    social = random.randint(20, 100)
    media = random.randint(20, 100)

    risk = (
        epidemiology * 0.4 +
        healthcare * 0.2 +
        social * 0.2 +
        media * 0.2
    )

    outbreak = 1 if risk > 70 else 0

    data.append({
        "Country": country,
        "Epidemiology": epidemiology,
        "Healthcare Strain": healthcare,
        "Social Disruption": social,
        "Media Signals": media,
        "Risk Score": round(risk, 2),
        "Outbreak": outbreak
    })

df = pd.DataFrame(data)

# -----------------------------
# AI ANOMALY DETECTION
# -----------------------------
model = IsolationForest(contamination=0.2, random_state=42)

features = df[[
    "Epidemiology",
    "Healthcare Strain",
    "Social Disruption",
    "Media Signals"
]]

df["AI Alert"] = model.fit_predict(features)

df["AI Alert"] = df["AI Alert"].apply(
    lambda x: "🚨 High Risk" if x == -1 else "🟢 Stable"
)

# -----------------------------
# SAVE TO DATABASE
# -----------------------------
for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO intelligence VALUES (?, ?, ?, ?)
    """, (
        row["Country"],
        float(row["Risk Score"]),
        int(row["Outbreak"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

conn.commit()

# -----------------------------
# GLOBAL METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries Monitored", len(df))
col2.metric("Outbreak Zones", int(df["Outbreak"].sum()))
col3.metric("Average Risk", round(df["Risk Score"].mean(), 2))
col4.metric("AI Engine", "ONLINE")

# -----------------------------
# ALERT SECTION
# -----------------------------
st.subheader("🚨 Active Global Alerts")

alerts = df[df["Outbreak"] == 1]

if len(alerts) == 0:
    st.success("No active outbreak alerts detected")
else:
    for _, row in alerts.iterrows():
        st.error(
            f"{row['Country']} — Risk Score: {row['Risk Score']}"
        )

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Global Intelligence Overview")

st.dataframe(df)

# -----------------------------
# RISK MAP
# -----------------------------
st.subheader("🌍 Global Risk Visualization")

fig = px.bar(
    df,
    x="Country",
    y="Risk Score",
    color="Risk Score",
    title="Global AI Risk Scores"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TREND ENGINE
# -----------------------------
st.subheader("📈 Global Trend Engine")

trend = pd.DataFrame({
    "Hour": range(1, 25),
    "Global Risk": np.random.randint(30, 90, 24)
})

fig2 = px.line(
    trend,
    x="Hour",
    y="Global Risk",
    title="24-Hour Global Risk Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ AI Signal Generator ]
          ↓
[ Risk Detection Engine ]
          ↓
[ SQLite Intelligence Memory ]
          ↓
[ WHO Alert Classification ]
          ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.success("WHO-style AI surveillance system operational")
