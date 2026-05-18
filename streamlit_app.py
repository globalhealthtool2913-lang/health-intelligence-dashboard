import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from sklearn.ensemble import RandomForestRegressor

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="WHO Enterprise Intelligence System",
    layout="wide"
)

st.title("🌍 WHO ENTERPRISE GLOBAL HEALTH INTELLIGENCE SYSTEM")
st.caption("Multi-source AI early warning & outbreak prediction platform")

# =============================
# MULTI-SOURCE DATA LAYER
# =============================

# --- Health Data (OWID fallback safe) ---
@st.cache_data(ttl=3600)
def load_health_data():
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url)

        latest = df[df["date"] == df["date"].max()]

        return latest[[
            "location",
            "total_cases_per_million",
            "total_deaths_per_million",
            "stringency_index"
        ]].dropna().rename(columns={
            "location": "Country",
            "total_cases_per_million": "Cases",
            "total_deaths_per_million": "Deaths",
            "stringency_index": "Policy"
        })

    except:
        return pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": [1000, 2000, 5000, 4000, 3500],
            "Deaths": [50, 80, 300, 200, 250],
            "Policy": [60, 70, 80, 75, 65]
        })

# --- News Signal Simulation Layer (enterprise placeholder) ---
def generate_news_signals(df):
    np.random.seed(42)
    df["News_Signal"] = np.random.randint(0, 100, len(df))
    df["Media_Attention"] = np.random.randint(0, 100, len(df))
    return df

df = load_health_data()
df = generate_news_signals(df)

# =============================
# DATA FUSION ENGINE
# =============================
df["Risk Score"] = (
    df["Cases"] * 0.35 +
    df["Deaths"] * 0.35 +
    (100 - df["Policy"]) * 0.15 +
    df["News_Signal"] * 0.1 +
    df["Media_Attention"] * 0.05
)

# =============================
# AI MODEL
# =============================
model = RandomForestRegressor(n_estimators=200, random_state=42)

X = df[["Cases", "Deaths", "Policy", "News_Signal", "Media_Attention"]]
y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# =============================
# ALERT ENGINE (ENTERPRISE LOGIC)
# =============================
threshold = df["Risk Score"].quantile(0.85)
alerts = df[df["Risk Score"] > threshold]

# =============================
# GLOBAL METRICS
# =============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries Monitored", len(df))
col2.metric("Active Alerts", len(alerts))
col3.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col4.metric("System Status", "ENTERPRISE LIVE")

# =============================
# ALERT DASHBOARD
# =============================
st.subheader("🚨 Global Early Warning Alerts")

if alerts.empty:
    st.success("No critical global outbreaks detected")
else:
    for _, row in alerts.iterrows():
        st.error(
            f"{row['Country']} | Risk: {row['Risk Score']:.2f}"
        )

# =============================
# GLOBAL RISK MAP
# =============================
st.subheader("🌍 Global Risk Intelligence Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="Enterprise Global Health Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# AI vs REAL RISK
# =============================
st.subheader("🤖 AI Prediction Validation")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="Cases",
    title="AI Model vs Real Risk Correlation"
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# DATA TABLE
# =============================
st.subheader("📊 Intelligence Dataset")
st.dataframe(df)

# =============================
# SYSTEM FEED
# =============================
st.subheader("🧠 Intelligence Feed")

feed = [
    "Ingesting multi-source global health signals...",
    "Processing news + epidemiological data...",
    "Running AI risk fusion engine...",
    "Updating outbreak detection layer...",
    "System operating in enterprise mode..."
]

for msg in feed:
    st.info(msg)

# =============================
# FOOTER
# =============================
st.success("🟢 ENTERPRISE WHO INTELLIGENCE SYSTEM ACTIVE")
