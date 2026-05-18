
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io

st.set_page_config(page_title="WHO Intelligence System", layout="wide")

st.title("🌍 WHO Multi-Source Intelligence System")
st.caption("AI + Health Data + Early Warning System")

# =========================
# SAFE DATA LOADER
# =========================
@st.cache_data(ttl=3600)
def load_health_data():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        df = pd.read_csv(io.StringIO(response.text))

    except Exception:

        st.warning("⚠️ Live data unavailable → using fallback dataset")

        df = pd.DataFrame({
            "location": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "total_cases_per_million": [1200, 2300, 5400, 4100, 3600],
            "total_deaths_per_million": [60, 90, 310, 210, 260],
            "stringency_index": [65, 72, 80, 78, 70]
        })

    latest = df[df["date"] == df["date"].max()] if "date" in df.columns else df

    latest = latest[[
        "location",
        "total_cases_per_million",
        "total_deaths_per_million",
        "stringency_index"
    ]].rename(columns={
        "location": "Country",
        "total_cases_per_million": "Cases",
        "total_deaths_per_million": "Deaths",
        "stringency_index": "Policy"
    }).dropna()

    return latest

# =========================
# LOAD DATA
# =========================
df = load_health_data()

# =========================
# RISK ENGINE
# =========================
df["Risk Score"] = (
    df["Cases"] * 0.3 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.3
)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(df))
col2.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col3.metric("Max Risk", round(df["Risk Score"].max(), 2))

# =========================
# ALERTS
# =========================
st.subheader("🚨 Global Alerts")

threshold = df["Risk Score"].quantile(0.85)
alerts = df[df["Risk Score"] > threshold]

if alerts.empty:
    st.success("No high-risk outbreaks detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → Risk: {row['Risk Score']:.2f}")

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="WHO Intelligence Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Intelligence Data")

st.dataframe(df)
