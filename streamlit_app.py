import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-21 Global Health Intelligence AI",
    layout="wide"
)

st.title("🌍 RW-21 AI-Powered Global Health Intelligence System")
st.caption("Production ML dashboard connected to backend intelligence engine")

# -----------------------------
# BACKEND
# -----------------------------
EVENTS_API = "http://localhost:8000/events"
PREDICT_API = "http://localhost:8000/predict"

# -----------------------------
# LOAD EVENTS
# -----------------------------
def load_events():

    try:
        res = requests.get(EVENTS_API, timeout=5)
        data = res.json()
        return pd.DataFrame(data) if data else pd.DataFrame()

    except:
        st.error("❌ Backend not running (RW-20/21 required)")
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
# ML PREDICTION VIEW (FROM BACKEND)
# -----------------------------
st.subheader("🧠 Machine Learning Prediction Engine")

if st.button("Run AI Prediction"):

    try:
        response = requests.post(PREDICT_API, json={
            "high": high,
            "moderate": moderate,
            "low": low
        }, timeout=5)

        result = response.json()

        risk_score = result.get("risk_score", 0)
        probability = result.get("probability", 0)

        st.metric("📊 Risk Score", round(risk_score, 2))
        st.metric("🔮 Outbreak Probability", f"{probability * 100:.1f}%")

        # ALERT LOGIC (DISPLAY ONLY)
        if probability >= 0.7:
            st.error("🚨 HIGH OUTBREAK RISK")
        elif probability >= 0.4:
            st.warning("⚠️ MODERATE RISK")
        else:
            st.success("🟢 LOW RISK")

    except:
        st.error("❌ Prediction API not available")

# -----------------------------
# TREND VIEW (FROM DATA)
# -----------------------------
st.subheader("📈 Trend Intelligence")

if not df.empty and "score" in df.columns:

    scores = df["score"].tolist()

    if len(scores) > 2:

        trend = scores[-1] - scores[-2]

        if trend > 0:
            st.warning("📈 Increasing Risk Trend")
        elif trend < 0:
            st.info("📉 Decreasing Risk Trend")
        else:
            st.success("➡️ Stable Trend")

    else:
        st.info("Not enough data for trend analysis")

# -----------------------------
# DATA TABLE
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
- System: RW-21 ML Intelligence Layer
- Backend: FastAPI required
- ML Engine: Server-side model
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
[ Feature Engineering Layer ]
        ↓
[ ML Model (RW-21) ]
        ↓
[ Prediction API ]
        ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-21 - Production AI Global Health Intelligence System")
