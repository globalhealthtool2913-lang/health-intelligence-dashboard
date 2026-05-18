import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import plotly.express as px

st.set_page_config(page_title="WHO Intelligence System", layout="wide")

st.title("🌍 WHO Multi-Source Intelligence System")
st.caption("Real-time Health + Risk + Early Warning System")

# =========================
# SAFE DATA LOADER
# =========================
@st.cache_data(ttl=3600)
def load_health_data():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    try:
        r = requests.get(url, timeout=20)
        df = pd.read_csv(io.StringIO(r.text))

        latest_date = df["date"].max()
        df = df[df["date"] == latest_date]

        df = df[[
            "location",
            "total_cases_per_million",
            "total_deaths_per_million",
            "stringency_index"
        ]].rename(columns={
            "location": "Country",
            "total_cases_per_million": "Cases",
            "total_deaths_per_million": "Deaths",
            "stringency_index": "Policy"
        })

    except Exception:
        st.warning("⚠️ Live data failed → using fallback dataset")

        df = pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        })

    return df.dropna()

# =========================
# LOAD DATA
# =========================
df = load_health_data()

# =========================
# VALIDATION (PREVENT ERRORS)
# =========================
required_cols = ["Cases", "Deaths", "Policy"]

for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()

# =========================
# RISK ENGINE
# =========================
df["Risk Score"] = (
    df["Cases"].astype(float) * 0.3 +
    df["Deaths"].astype(float) * 0.4 +
    (100 - df["Policy"].astype(float)) * 0.3
)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(df))
col2.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col3.metric("Max Risk", round(df["Risk Score"].max(), 2))

# =========================
# ALERT SYSTEM
# =========================
st.subheader("🚨 Global Alerts")

threshold = df["Risk Score"].quantile(0.85)
alerts = df[df["Risk Score"] > threshold]

if alerts.empty:
    st.success("🟢 No active outbreak signals")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → Risk {row['Risk Score']:.2f}")

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
