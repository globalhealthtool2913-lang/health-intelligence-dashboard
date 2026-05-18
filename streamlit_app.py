import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="WHO Real-Time Intelligence System", layout="wide")

st.title("🌍 WHO Real-Time Intelligence System")
st.caption("Live Health + News + AI Fusion Engine")

# =========================
# AUTO REFRESH OPTION
# =========================
refresh = st.sidebar.button("🔄 Refresh Data")

# =========================
# REAL HEALTH DATA (LIVE)
# =========================
def load_health_data():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    try:
        r = requests.get(url, timeout=15)
        df = pd.read_csv(io.StringIO(r.text))

    except Exception:
        st.warning("⚠️ Live data failed → fallback activated")

        return pd.DataFrame({
            "location": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "total_cases_per_million": np.random.randint(1000, 5000, 5),
            "total_deaths_per_million": np.random.randint(50, 300, 5),
            "stringency_index": np.random.randint(40, 90, 5)
        })

    latest_date = df["date"].max()
    latest = df[df["date"] == latest_date]

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
# REAL-TIME NEWS SIGNAL (SIMULATED LIVE FEED)
# =========================
def load_news_signals(df):

    np.random.seed(int(datetime.now().timestamp()) % 1000)

    df["News_Intensity"] = np.random.randint(0, 100, len(df))
    df["Outbreak_Signal"] = np.random.randint(0, 100, len(df))

    return df

# =========================
# REFRESH LOGIC
# =========================
df = load_health_data()

if refresh:
    st.cache_data.clear()
    df = load_health_data()

df = load_news_signals(df)

# =========================
# REAL-TIME RISK ENGINE
# =========================
df["Risk Score"] = (
    df["Cases"] * 0.3 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.2 +
    df["News_Intensity"] * 0.1 +
    df["Outbreak_Signal"] * 0.1
)

# =========================
# LIVE METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(df))
col2.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col3.metric("Max Risk", round(df["Risk Score"].max(), 2))

# =========================
# ALERT ENGINE
# =========================
st.subheader("🚨 Live Outbreak Alerts")

threshold = df["Risk Score"].quantile(0.85)
alerts = df[df["Risk Score"] > threshold]

if alerts.empty:
    st.success("🟢 No active outbreak signals")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → Risk {row['Risk Score']:.2f}")

# =========================
# REAL-TIME MAP
# =========================
st.subheader("🌍 Live Global Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="Real-Time WHO Intelligence Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Live Intelligence Feed")

st.dataframe(df)
