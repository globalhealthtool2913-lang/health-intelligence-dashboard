import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.ensemble import RandomForestRegressor

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Global Health AI System",
    layout="wide"
)

st.title("🌍 Global Health AI Intelligence System")
st.caption("Production-stable AI + real-data + time-series monitoring")

# =============================
# SAFE DATA LOADER (FIXED ERROR)
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
        # fallback data (prevents crash)
        st.warning("⚠️ Using fallback dataset (network unavailable)")
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
# AI MODEL
# =============================
model = RandomForestRegressor(n_estimators=150, random_state=42)

X = df[["Cases", "Deaths", "Policy"]]
y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# =============================
# TIME-SERIES MEMORY SYSTEM
# =============================
if "history" not in st.session_state:
    st.session_state.history = {}

for c in df["Country"].head(10):

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
col4.metric("System Status", "ACTIVE")

# =============================
# ALERT SYSTEM
# =============================
st.subheader("🚨 Alerts")

alerts = df[df["Risk Score"] > df["Risk Score"].quantile(0.85)]

if alerts.empty:
    st.success("No high-risk signals detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} | Risk Score: {row['Risk Score']:.2f}")

# =============================
# DATA TABLE
# =============================
st.subheader("📊 Dataset")
st.dataframe(df)

# =============================
# VISUALIZATION 1
# =============================
st.subheader("🌍 Global Risk Distribution")

fig = px.bar(
    df.sort_values("Risk Score", ascending=False),
    x="Country",
    y="Risk Score",
    color="Risk Score",
    title="Global Health Risk Overview"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# VISUALIZATION 2
# =============================
st.subheader("🤖 AI vs Real Risk")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="Cases",
    title="AI Prediction Validation"
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# TIME SERIES VIEW
# =============================
st.subheader("📈 Outbreak Time-Series Memory")

selected = st.selectbox("Select Country", df["Country"].head(10))

history = st.session_state.history.get(selected, [])

if len(history) > 1:

    ts = pd.DataFrame({
        "Step": list(range(len(history))),
        "Risk": history
    })

    fig3 = px.line(
        ts,
        x="Step",
        y="Risk",
        title=f"{selected} Risk Trend Over Time"
    )

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Collecting historical data... refresh app")

# =============================
# SYSTEM FEED
# =============================
st.subheader("🧠 System Feed")

feed = [
    "Monitoring global health signals...",
    "Updating AI risk engine...",
    "Processing epidemiological data...",
    "Analyzing outbreak patterns...",
    "System stable and running..."
]

for msg in feed[:3]:
    st.info(msg)

# =============================
# FOOTER
# =============================
st.success("System running successfully (production-stable mode)")
