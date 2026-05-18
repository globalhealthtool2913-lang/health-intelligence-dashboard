import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import plotly.express as px

st.set_page_config(page_title="WHO AI Forecast System", layout="wide")

st.title("🌍 WHO AI Intelligence + Forecasting System")
st.caption("Real-time outbreak detection + AI time-series forecasting")

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
# 🧠 ANOMALY DETECTION
# =========================
mean_risk = df["Risk Score"].mean()
std_risk = df["Risk Score"].std()

df["Anomaly Score"] = (df["Risk Score"] - mean_risk) / (std_risk + 1e-6)
df["Anomaly"] = df["Anomaly Score"].apply(lambda x: abs(x) > 1.5)

# =========================
# 📈 FORECASTING ENGINE (TIME SERIES AI)
# =========================

def forecast_risk(series, steps=5):

    # simple AI trend model (rolling slope approximation)
    x = np.arange(len(series))
    y = series.values

    if len(series) < 2:
        return [series.mean()] * steps

    # linear regression (manual)
    slope = np.polyfit(x, y, 1)[0]

    last_value = y[-1]

    forecast = []
    for i in range(1, steps + 1):
        forecast.append(last_value + slope * i)

    return forecast

# Create synthetic time series per country
st.subheader("📈 AI Forecasting (Next 5 Steps)")

forecast_results = []

for _, row in df.iterrows():

    history = np.array([
        row["Risk Score"] * np.random.uniform(0.8, 1.0),
        row["Risk Score"] * np.random.uniform(0.9, 1.1),
        row["Risk Score"]
    ])

    future = forecast_risk(pd.Series(history), steps=5)

    forecast_results.append({
        "Country": row["Country"],
        "Next_Risk": future[-1]
    })

forecast_df = pd.DataFrame(forecast_results)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(df))
col2.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col3.metric("Max Forecast Risk", round(forecast_df["Next_Risk"].max(), 2))

# =========================
# ALERT SYSTEM
# =========================
st.subheader("🚨 AI Alerts (Anomaly Detection)")

alerts = df[df["Anomaly"] == True]

if alerts.empty:
    st.success("🟢 No anomalies detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → Risk {row['Risk Score']:.2f} (ANOMALY)")

# =========================
# FORECAST DISPLAY
# =========================
st.subheader("📊 Forecasted Risk (Next Period)")

fig2 = px.bar(
    forecast_df,
    x="Country",
    y="Next_Risk",
    title="AI Predicted Outbreak Risk"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 Current Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="WHO AI Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE
# =========================
st.subheader("📊 Intelligence Data")

st.dataframe(df)
