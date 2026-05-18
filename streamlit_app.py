import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import sqlite3
import random

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="WHO Global Health Intelligence",
    layout="wide"
)

# -----------------------------------
# AUTO REFRESH
# -----------------------------------
st_autorefresh(interval=15000, key="who_refresh")

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🏥 WHO GLOBAL HEALTH INTELLIGENCE & OUTBREAK PREDICTION SYSTEM")
st.caption("AI-Powered Global Surveillance & Early Warning Platform")

# -----------------------------------
# DATABASE
# -----------------------------------
conn = sqlite3.connect("who_global_health.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS intelligence (
    country TEXT,
    risk REAL,
    level TEXT,
    outbreak INTEGER,
    timestamp TEXT
)
""")

conn.commit()

# -----------------------------------
# COUNTRIES
# -----------------------------------
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

# -----------------------------------
# RISK CLASSIFICATION
# -----------------------------------
def classify_risk(score):
    if score >= 80:
        return "🔴 Critical"
    elif score >= 65:
        return "🟠 High"
    elif score >= 45:
        return "🟡 Moderate"
    else:
        return "🟢 Low"

# -----------------------------------
# SIGNAL GENERATION
# -----------------------------------
records = []

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

    prediction = min(
        100,
        round(
            (epidemiology * 0.5) +
            (healthcare * 0.3) +
            (social * 0.2),
            2
        )
    )

    level = classify_risk(risk)

    records.append({
        "Country": country,
        "Epidemiology": epidemiology,
        "Healthcare": healthcare,
        "Social": social,
        "Media": media,
        "Risk Score": round(risk, 2),
        "Risk Level": level,
        "Outbreak Prediction %": prediction,
        "Outbreak": outbreak
    })

df = pd.DataFrame(records)

# -----------------------------------
# AI ANOMALY DETECTION
# -----------------------------------
model = IsolationForest(
    contamination=0.2,
    random_state=42
)

features = df[[
    "Epidemiology",
    "Healthcare",
    "Social",
    "Media"
]]

df["AI Status"] = model.fit_predict(features)

df["AI Status"] = df["AI Status"].apply(
    lambda x: "🚨 Escalating" if x == -1 else "🟢 Stable"
)

# -----------------------------------
# SAVE TO DATABASE
# -----------------------------------
for _, row in df.iterrows():

    cursor.execute("""
    INSERT INTO intelligence VALUES (?, ?, ?, ?, ?)
    """, (
        row["Country"],
        float(row["Risk Score"]),
        row["Risk Level"],
        int(row["Outbreak"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

conn.commit()

# -----------------------------------
# METRICS
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries Monitored", len(df))
col2.metric("Outbreak Zones", int(df["Outbreak"].sum()))
col3.metric("Average Global Risk", round(df["Risk Score"].mean(), 2))
col4.metric("AI Surveillance", "ONLINE")

# -----------------------------------
# ALERTS
# -----------------------------------
st.subheader("🚨 Active Global Alerts")

alerts = df[df["Outbreak"] == 1]

if len(alerts) == 0:
    st.success("No active outbreak alerts detected")

else:
    for _, row in alerts.iterrows():

        st.error(
            f"{row['Country']} | "
            f"{row['Risk Level']} | "
            f"Prediction: {row['Outbreak Prediction %']}%"
        )

# -----------------------------------
# INTELLIGENCE FEED
# -----------------------------------
st.subheader("🧠 Live Intelligence Feed")

feed = [
    "AI detected elevated respiratory signals in East Africa",
    "Cross-border outbreak probability increased",
    "Healthcare strain rising in multiple regions",
    "Early epidemic acceleration patterns detected",
    "AI surveillance detected abnormal epidemiological activity"
]

for item in random.sample(feed, 3):
    st.info(item)

# -----------------------------------
# DATA TABLE
# -----------------------------------
st.subheader("📊 Global Intelligence Overview")

st.dataframe(df)

# -----------------------------------
# GLOBAL RISK BAR
# -----------------------------------
st.subheader("🌍 Global Risk Visualization")

fig = px.bar(
    df,
    x="Country",
    y="Risk Score",
    color="Risk Score",
    hover_data=["Risk Level", "Outbreak Prediction %"],
    title="Global AI Risk Scores"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# HEATMAP
# -----------------------------------
st.subheader("🗺️ WHO Global Risk Heatmap")

map_fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    hover_name="Country",
    color_continuous_scale="Reds",
    title="AI Global Outbreak Risk Map"
)

st.plotly_chart(map_fig, use_container_width=True)

# -----------------------------------
# TREND ENGINE
# -----------------------------------
st.subheader("📈 Global Trend Engine")

trend = pd.DataFrame({
    "Hour": range(1, 25),
    "Global Risk": np.random.randint(30, 95, 24)
})

trend_fig = px.line(
    trend,
    x="Hour",
    y="Global Risk",
    title="24-Hour Global Risk Trend"
)

st.plotly_chart(trend_fig, use_container_width=True)

# -----------------------------------
# HISTORICAL MEMORY
# -----------------------------------
st.subheader("🗄️ Historical Intelligence Memory")

history = pd.read_sql_query(
    "SELECT * FROM intelligence ORDER BY timestamp DESC LIMIT 20",
    conn
)

st.dataframe(history)

# -----------------------------------
# SYSTEM ARCHITECTURE
# -----------------------------------
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
[ Streamlit Intelligence Dashboard ]
""")

# -----------------------------------
# FOOTER
# -----------------------------------
st.success(
    "WHO-style AI outbreak prediction system operational"
)
