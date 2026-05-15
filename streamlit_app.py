import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-22 Global Health ML System",
    layout="wide"
)

st.title("🌍 RW-22 Real ML Global Health Intelligence System")
st.caption("Dataset-trained ML pipeline dashboard")

# -----------------------------
# BACKEND
# -----------------------------
EVENTS_API = "http://localhost:8000/events"
PREDICT_API = "http://localhost:8000/predict"

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    try:
        res = requests.get(EVENTS_API, timeout=5)
        return pd.DataFrame(res.json()) if res.json() else pd.DataFrame()
    except:
        st.error("❌ Backend not running (RW-22 required)")
        return pd.DataFrame()

df = load_data()

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

    high = (df["risk"] == "HIGH").sum()
    moderate = (df["risk"] == "MODERATE").sum()
    low = (df["risk"] == "LOW").sum()

else:
    high = moderate = low = 0

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ML PREDICTION (REAL MODEL OUTPUT)
# -----------------------------
st.subheader("🧠 ML Prediction Engine (RW-22)")

if st.button("Run Prediction"):

    try:
        response = requests.post(PREDICT_API, json={
            "high": high,
            "moderate": moderate,
            "low": low
        }, timeout=5)

        result = response.json()

        risk_score = result.get("risk_score", 0)

        st.metric("📊 Predicted Risk Score", round(risk_score, 2))

        if risk_score > 8:
            st.error("🚨 HIGH RISK DETECTED")
        elif risk_score > 5:
            st.warning("⚠️ MODERATE RISK")
        else:
            st.success("🟢 LOW RISK")

    except:
        st.error("❌ Prediction service unavailable")

# -----------------------------
# TREND ANALYSIS (FROM DATASET)
# -----------------------------
st.subheader("📈 Trend Intelligence")

if not df.empty and "risk" in df.columns:

    values = []

    for r in df["risk"]:
        if r == "HIGH":
            values.append(3)
        elif r == "MODERATE":
            values.append(2)
        else:
            values.append(1)

    if len(values) > 2:

        change = values[-1] - values[-2]

        if change > 0:
            st.warning("📈 Increasing Risk Trend")
        elif change < 0:
            st.info("📉 Decreasing Risk Trend")
        else:
            st.success("➡️ Stable Trend")

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Dataset")

if df.empty:
    st.warning("No backend data available")
else:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# SYSTEM STATUS
# -----------------------------
st.subheader("⚙️ System Status")

st.write(f"""
- System: RW-22 ML Training Pipeline Dashboard
- Backend: FastAPI required
- Model Type: RandomForest Regressor (server-side)
- Data: Dataset-trained
- Country: {country}
""")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Real Dataset Sources ]
        ↓
[ Data Cleaning + Feature Engineering ]
        ↓
[ ML Training (RW-22 Model) ]
        ↓
[ FastAPI Prediction Service ]
        ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-22 - Real ML Global Health Intelligence System")
