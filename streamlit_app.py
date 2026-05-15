import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-20 Global Health AI System",
    layout="wide"
)

st.title("🌍 RW-20 AI Global Health Prediction System")
st.caption("Machine Learning-powered outbreak prediction dashboard")

# -----------------------------
# BACKEND API
# -----------------------------
API_URL = "http://localhost:8000/events"
PREDICT_URL = "http://localhost:8000/predict"

# -----------------------------
# LOAD EVENTS
# -----------------------------
def load_events():
    try:
        res = requests.get(API_URL, timeout=5)
        data = res.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except:
        st.error("❌ Backend not running (FastAPI required)")
        return pd.DataFrame()

df = load_events()

# -----------------------------
# COUNTRY FILTER
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
if not df.empty and "risk" in df.columns:

    high = sum(df["risk"] == "HIGH")
    moderate = sum(df["risk"] == "MODERATE")
    low = sum(df["risk"] == "LOW")

else:
    high = moderate = low = 0

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# AI PREDICTION (RW-20 CORE)
# -----------------------------
st.subheader("🧠 AI Outbreak Prediction Engine")

if st.button("Run Prediction"):

    try:
        response = requests.post(PREDICT_URL, json={
            "high": high,
            "moderate": moderate,
            "low": low
        }, timeout=5)

        result = response.json()

        risk_score = result.get("risk_score", 0)
        probability = result.get("probability", 0)

        st.metric("📊 Risk Score", round(risk_score, 2))
        st.metric("🔮 Outbreak Probability", f"{probability * 100:.1f}%")

        if probability > 0.7:
            st.error("🚨 HIGH OUTBREAK RISK PREDICTED")
        elif probability > 0.4:
            st.warning("⚠️ MODERATE RISK DETECTED")
        else:
            st.success("🟢 LOW RISK")

    except:
        st.error("❌ Prediction service not available")

# -----------------------------
# DATA VIEW
# -----------------------------
st.subheader("📊 Intelligence Feed")

if df.empty:
    st.warning("No data from backend")
else:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# SYSTEM STATUS
# -----------------------------
st.subheader("⚙️ System Status")

st.write(f"""
- System: RW-20 AI Prediction Layer
- Backend: FastAPI required
- ML Model: Active (server-side)
- Country: {country}
""")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Live Data Sources ]
        ↓
[ FastAPI Backend ]
        ↓
[ ML Prediction Engine (RW-20) ]
        ↓
[ Prediction API ]
        ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-20 - AI-Powered Global Health Prediction System")
