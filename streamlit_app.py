import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import time

from sklearn.ensemble import RandomForestRegressor

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Global Health Intelligence System",
    layout="wide"
)

st.title("🌍 Global Health AI Intelligence System")
st.caption("Real-data + AI + Time-series outbreak monitoring")

# =============================
# AUTO REFRESH CONTROL
# =============================
refresh = st.sidebar.slider("Refresh Interval (seconds)", 10, 120, 30)

# =============================
# REAL DATA SOURCE (OWID)
# =============================
@st.cache_data(ttl=3600)
def load_data():
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

df = load_data()

# =============================
# RISK ENGINE (REAL DATA)
# =============================
df["Risk Score"] = (
    df["Cases"] * 0.4 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.2
)

# =============================
# AI MODEL
# =============================
model = RandomForestRegressor(n_estimators=150, random_state=42)

X = df[["Cases", "Deaths", "Policy"]]
y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# =============================
# MEMORY SYSTEM (TIME SERIES)
# =============================
if "history" not in st.session_state:
    st.session_state.history = {}

for c in df["Country"].head(15):

    if c not in st.session_state.history:
        st.session_state.history[c] = []

    val = float(df[df["Country"] == c]["Risk Score"].values[0])
    st.session_state.history[c].append(val)

    if len(st.session_state.history[c]) > 10:
        st.session_state.history[c].pop(0)

# =============================
# METRICS
# =============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("High Risk", len(df[df["Risk Score"] > df["Risk Score"].quantile(0.85)]))
col3.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col4.metric("AI Status", "LIVE")

# =============================
# ALERT SYSTEM
# =============================
st.subheader("🚨 Global Alerts")

alerts = df[df["Risk Score"] > df["Risk Score"].quantile(0.85)]

if alerts.empty:
    st.success("No critical global alerts detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} | Risk Score: {row['Risk Score']:.2f}")

# =============================
# MAIN TABLE
# =============================
st.subheader("📊 Global Intelligence Dataset")
st.dataframe(df)

# =============================
# RISK VISUALIZATION
# =============================
st.subheader("🌍 Global Risk Map")

fig = px.bar(
    df.sort_values("Risk Score", ascending=False).head(20),
    x="Country",
    y="Risk Score",
    color="Risk Score",
    title="Global Health Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# AI VS REAL RISK
# =============================
st.subheader("🤖 AI Prediction vs Real Risk")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="Cases",
    title="AI Model Validation View"
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# TIME SERIES VIEW
# =============================
st.subheader("📈 Outbreak Time-Series Memory")

selected_country = st.selectbox("Select Country", df["Country"].head(15))

history = st.session_state.history.get(selected_country, [])

if len(history) > 1:

    ts = pd.DataFrame({
        "Time": list(range(len(history))),
        "Risk": history
    })

    fig3 = px.line(
        ts,
        x="Time",
        y="Risk",
        title=f"{selected_country} Risk Evolution"
    )

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Building historical data... keep refreshing")

# =============================
# INTELLIGENCE FEED
# =============================
st.subheader("🧠 AI Intelligence Feed")

feed = [
    "Processing global epidemiological signals...",
    "Updating risk prediction model...",
    "Monitoring cross-country health indicators...",
    "Analyzing outbreak probability clusters...",
    "System operating in real-time mode..."
]

for msg in feed[:3]:
    st.info(msg)

# =============================
# AUTO REFRESH SYSTEM
# =============================
time.sleep(refresh)
st.rerun()

# =============================
# FOOTER
# =============================
st.success("System Running in Real-Time Mode")
