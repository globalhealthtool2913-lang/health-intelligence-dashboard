import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from sklearn.ensemble import RandomForestRegressor

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="WHO Intelligence System",
    layout="wide"
)

st.title("🌍 WHO Global Health Intelligence System")
st.caption("AI + Forecasting + Persistent Surveillance + Anomaly Detection")

# =============================
# HISTORY STORAGE
# =============================
HISTORY_FILE = "risk_history.csv"

# =============================
# SAFE DATA LOADER
# =============================
@st.cache_data(ttl=3600)
def load_data():

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

    except Exception:

        st.warning("⚠️ Using fallback data")

        return pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": [1000, 2000, 5000, 4000, 3500],
            "Deaths": [50, 80, 300, 200, 250],
            "Policy": [60, 70, 80, 75, 65]
        })

df = load_data()

# =============================
# RISK ENGINE
# =============================
df["Risk Score"] = (
    df["Cases"] * 0.4 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.2
)

# =============================
# SAVE HISTORY
# =============================
history_df = df[["Country", "Risk Score"]].copy()

history_df["Timestamp"] = pd.Timestamp.now()

if os.path.exists(HISTORY_FILE):

    old = pd.read_csv(HISTORY_FILE)

    combined = pd.concat([old, history_df])

    combined = combined.tail(1000)

    combined.to_csv(HISTORY_FILE, index=False)

else:

    history_df.to_csv(HISTORY_FILE, index=False)

# =============================
# LOAD HISTORY
# =============================
history_data = pd.read_csv(HISTORY_FILE)

# =============================
# AI MODEL
# =============================
model = RandomForestRegressor(
    n_estimators=150,
    random_state=42
)

X = df[["Cases", "Deaths", "Policy"]]
y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# =============================
# ALERT SYSTEM
# =============================
threshold = df["Risk Score"].quantile(0.85)

alerts = df[df["Risk Score"] > threshold]

# =============================
# METRICS
# =============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("Alerts", len(alerts))
col3.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col4.metric("System", "ACTIVE")

# =============================
# ALERT DISPLAY
# =============================
st.subheader("🚨 Global Alerts")

if alerts.empty:

    st.success("No major outbreak alerts detected")

else:

    for _, row in alerts.iterrows():

        st.error(
            f"{row['Country']} | Risk Score: {row['Risk Score']:.2f}"
        )

# =============================
# ANOMALY DETECTION ENGINE
# =============================
st.subheader("⚠️ Outbreak Anomaly Detection")

anomalies = []

for country in df["Country"].unique():

    country_history = history_data[
        history_data["Country"] == country
    ]

    if len(country_history) > 5:

        recent = country_history.tail(5)["Risk Score"].values

        mean_risk = np.mean(recent[:-1])

        latest_risk = recent[-1]

        # Spike threshold
        if latest_risk > mean_risk * 1.25:

            spike = (
                (latest_risk - mean_risk)
                / mean_risk
            ) * 100

            anomalies.append({
                "Country": country,
                "Spike %": round(spike, 2),
                "Current Risk": round(latest_risk, 2)
            })

# =============================
# DISPLAY ANOMALIES
# =============================
if len(anomalies) == 0:

    st.success("No abnormal outbreak spikes detected")

else:

    anomaly_df = pd.DataFrame(anomalies)

    for _, row in anomaly_df.iterrows():

        st.warning(
            f"{row['Country']} anomaly detected | "
            f"Spike: {row['Spike %']}%"
        )

    st.dataframe(anomaly_df)

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
# AI VALIDATION
# =============================
st.subheader("🤖 AI Prediction Validation")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="Cases",
    title="AI Prediction vs Real Risk"
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# DATA TABLE
# =============================
st.subheader("📊 Intelligence Dataset")

st.dataframe(df)

# =============================
# FORECAST ENGINE
# =============================
st.subheader("📈 Forecast Engine")

selected_country = st.selectbox(
    "Select Country",
    df["Country"].unique()
)

country_history = history_data[
    history_data["Country"] == selected_country
]

if len(country_history) > 3:

    country_history = country_history.tail(10)

    risks = country_history["Risk Score"].values

    trend = np.polyfit(
        range(len(risks)),
        risks,
        1
    )

    future_steps = list(
        range(len(risks), len(risks) + 5)
    )

    forecast = [
        trend[0] * x + trend[1]
        for x in future_steps
    ]

    forecast_df = pd.DataFrame({
        "Future Step": future_steps,
        "Forecast Risk": forecast
    })

    fig_forecast = px.line(
        forecast_df,
        x="Future Step",
        y="Forecast Risk",
        title=f"{selected_country} Forecasted Risk"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

else:

    st.info("Collecting more historical data...")

# =============================
# HISTORICAL TREND
# =============================
st.subheader("📈 Historical Risk Trend")

trend_history = country_history.tail(20)

if len(trend_history) > 1:

    fig3 = px.line(
        trend_history,
        x="Timestamp",
        y="Risk Score",
        title=f"{selected_country} Historical Risk Trend"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =============================
# INTELLIGENCE FEED
# =============================
st.subheader("🧠 Intelligence Feed")

feed = [
    "Monitoring global outbreak acceleration...",
    "Analyzing anomaly signals...",
    "Updating forecasting engine...",
    "Tracking epidemiological shifts...",
    "Persistent surveillance active..."
]

for msg in feed:

    st.info(msg)

# =============================
# FOOTER
# =============================
st.success(
    "🟢 Persistent WHO Surveillance System Active"
)
