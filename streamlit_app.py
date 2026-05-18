import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests

st.set_page_config(page_title="WHO Production Intelligence System", layout="wide")

st.title("🌍 WHO Production Global Intelligence System")
st.caption("Real-world architecture simulation (frontend dashboard)")

# =============================
# LOAD FROM BACKEND API (SIMULATED)
# =============================
@st.cache_data(ttl=60)
def load_backend_data():
    # In real system → FastAPI endpoint
    # Example: http://backend:8000/risks

    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url)

        latest = df[df["date"] == df["date"].max()]

        latest = latest[[
            "location",
            "total_cases_per_million",
            "total_deaths_per_million",
            "stringency_index"
        ]].dropna()

        latest = latest.rename(columns={
            "location": "Country",
            "total_cases_per_million": "Cases",
            "total_deaths_per_million": "Deaths",
            "stringency_index": "Policy"
        })

        return latest

    except:
        return pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India"],
            "Cases": [1000, 2000, 5000, 4000],
            "Deaths": [50, 80, 300, 200],
            "Policy": [60, 70, 80, 75]
        })

df = load_backend_data()

# =============================
# RISK ENGINE (PRODUCTION LOGIC)
# =============================
df["Risk Score"] = (
    df["Cases"] * 0.4 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.2
)

# =============================
# ALERT SYSTEM (PRODUCTION RULES)
# =============================
threshold = df["Risk Score"].quantile(0.85)
alerts = df[df["Risk Score"] > threshold]

# =============================
# METRICS
# =============================
col1, col2, col3 = st.columns(3)

col1.metric("Countries Monitored", len(df))
col2.metric("Active Alerts", len(alerts))
col3.metric("System Mode", "PRODUCTION SIM")

# =============================
# ALERT DISPLAY
# =============================
st.subheader("🚨 Early Warning Alerts")

if alerts.empty:
    st.success("No critical global alerts detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} | Risk Score: {row['Risk Score']:.2f}")

# =============================
# GLOBAL MAP
# =============================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="Global Health Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# DATA TABLE
# =============================
st.subheader("📊 Intelligence Data")
st.dataframe(df)

st.success("System running in production simulation mode")
