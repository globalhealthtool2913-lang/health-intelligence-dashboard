import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import plotly.express as px

st.set_page_config(page_title="WHO AI Intelligence System", layout="wide")

st.title("🌍 WHO AI Intelligence System (Anomaly Detection)")
st.caption("Real-time outbreak monitoring + AI anomaly detection")

# =========================
# DATA LOADER
# =========================
@st.cache_data(ttl=3600)
def load_health_data():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    try:
        r = requests.get(url, timeout=20)
        df = pd.read_csv(io.StringIO(r.text))

        latest = df[df["date"] == df["date"].max()]

        df = latest[[
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

    except Exception:

        st.warning("⚠️ Using fallback dataset")

        df = pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        })

    return df

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
# 🧠 AI ANOMALY DETECTION ENGINE
# =========================

mean_risk = df["Risk Score"].mean()
std_risk = df["Risk Score"].std()

df["Anomaly Score"] = (df["Risk Score"] - mean_risk) / (std_risk + 1e-6)

df["Anomaly Flag"] = df["Anomaly Score"].apply(
    lambda x: "🚨 ANOMALY" if abs(x) > 1.5 else "OK"
)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(df))
col2.metric("Avg Risk", round(mean_risk, 2))
col3.metric("Max Risk", round(df["Risk Score"].max(), 2))

# =========================
# ALERTS
# =========================
st.subheader("🚨 Outbreak Alerts")

alerts = df[df["Anomaly Flag"] == "🚨 ANOMALY"]

if alerts.empty:
    st.success("🟢 No anomaly detected")
else:
    for _, row in alerts.iterrows():
        st.error(
            f"{row['Country']} → Risk {row['Risk Score']:.2f} | "
            f"Anomaly Score: {row['Anomaly Score']:.2f}"
        )

# =========================
# MAP
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="WHO AI Risk Map with Anomaly Detection"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Intelligence Table")

st.dataframe(df)
