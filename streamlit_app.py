import streamlit as st
import requests
import pandas as pd
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-19 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-19 Predictive Global Health Intelligence System")
st.caption("AI-ready analytics dashboard (connected to RW-18 backend)")

# -----------------------------
# BACKEND
# -----------------------------
API_URL = "http://localhost:8000/events"

def load_data():

    try:
        res = requests.get(API_URL, timeout=5)
        data = res.json()

        if not data:
            return pd.DataFrame()

        return pd.DataFrame(data)

    except:
        st.error("❌ Backend not reachable (RW-18 required)")
        return pd.DataFrame()

df = load_data()

# -----------------------------
# FILTER
# -----------------------------
if not df.empty and "country" in df.columns:

    country = st.sidebar.selectbox(
        "Select Country",
        sorted(df["country"].unique())
    )

    df = df[df["country"] == country]

else:
    country = "N/A"

# -----------------------------
# METRICS
# -----------------------------
if not df.empty and "score" in df.columns:

    scores = df["score"].tolist()

    high = sum(df["risk"] == "HIGH")
    moderate = sum(df["risk"] == "MODERATE")
    low = sum(df["risk"] == "LOW")

else:
    scores = []
    high = moderate = low = 0

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ANOMALY DETECTION (RW-19 CORE)
# -----------------------------
st.subheader("🧠 Anomaly Detection Engine")

if len(scores) > 2:

    mean = np.mean(scores)
    std = np.std(scores)
    threshold = mean + 2 * std

    latest = scores[-1]

    if latest > threshold:
        st.error("🚨 ANOMALY DETECTED: Unusual spike in health signals")
    else:
        st.success("🟢 No anomaly detected")

    st.write(f"- Mean Score: {mean:.2f}")
    st.write(f"- Threshold: {threshold:.2f}")
    st.write(f"- Latest Score: {latest}")

else:
    st.info("Not enough data for anomaly detection")

# -----------------------------
# TREND ANALYSIS
# -----------------------------
st.subheader("📈 Trend Intelligence")

if len(scores) > 1:

    if scores[-1] > scores[-2]:
        st.warning("📈 Increasing Risk Trend")
        trend = "UP"
    elif scores[-1] < scores[-2]:
        st.info("📉 Decreasing Risk Trend")
        trend = "DOWN"
    else:
        st.success("➡️ Stable Trend")
        trend = "STABLE"

else:
    trend = "UNKNOWN"
    st.info("Not enough data for trend analysis")

# -----------------------------
# SIMPLE FORECAST
# -----------------------------
st.subheader("🔮 Forecast (Simple Model)")

if len(scores) >= 3:

    forecast = np.mean(scores[-3:])
    st.write(f"Predicted Next Risk Score: **{forecast:.2f}**")

else:
    st.info("Not enough data for forecast")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")

if df.empty:
    st.warning("No backend data available")
else:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# SYSTEM STATUS
# -----------------------------
st.subheader("⚙️ System Status")

st.write(f"""
- System: RW-19 Predictive Intelligence Layer
- Backend: RW-18 FastAPI required
- Country: {country}
- Trend: {trend}
""")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Live Data Sources ]
        ↓
[ Ingestion Layer (RW-18 Backend) ]
        ↓
[ Storage (Database) ]
        ↓
[ AI Layer (RW-19: Anomaly + Trend + Forecast) ]
        ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-19 - Predictive Intelligence Dashboard")
