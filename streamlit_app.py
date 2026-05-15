import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence", layout="wide")

st.title("🌍 Global Health Intelligence System")
st.caption("AI-powered surveillance dashboard (production-ready structure)")

# -----------------------------
# BACKEND URL (CHANGE THIS IN DEPLOYMENT)
# -----------------------------
API_BASE = "http://localhost:8000"

# -----------------------------
# SAFE REQUESTS (NO BREAKS)
# -----------------------------
def get_events():
    try:
        return requests.get(f"{API_BASE}/events", timeout=3).json()
    except:
        return None

def get_prediction(payload):
    try:
        return requests.post(f"{API_BASE}/predict", json=payload, timeout=3).json()
    except:
        return None

# -----------------------------
# LOAD DATA
# -----------------------------
raw = get_events()

if raw:
    df = pd.DataFrame(raw)
    backend_status = "🟢 LIVE BACKEND"
else:
    df = pd.DataFrame([
        {"country": "Ethiopia", "risk": "HIGH", "score": 9},
        {"country": "Kenya", "risk": "MODERATE", "score": 5},
        {"country": "Uganda", "risk": "LOW", "score": 2}
    ])
    backend_status = "🔴 OFFLINE (USING SAMPLE DATA)"

# -----------------------------
# STATUS
# -----------------------------
st.subheader("⚙️ System Status")
st.write(f"Backend Status: {backend_status}")

# -----------------------------
# COUNTRY FILTER
# -----------------------------
if "country" in df.columns:
    country = st.sidebar.selectbox("Select Country", df["country"].unique())
    df = df[df["country"] == country]

# -----------------------------
# METRICS
# -----------------------------
high = (df["risk"] == "HIGH").sum()
moderate = (df["risk"] == "MODERATE").sum()
low = (df["risk"] == "LOW").sum()

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ML PREDICTION SECTION
# -----------------------------
st.subheader("🧠 AI Prediction Engine")

if st.button("Run Prediction"):

    result = get_prediction({
        "high": int(high),
        "moderate": int(moderate),
        "low": int(low)
    })

    if result:
        st.metric("📊 Risk Score", round(result["risk_score"], 2))
        st.metric("🔮 Probability", round(result["probability"], 2))

        if result["probability"] > 0.7:
            st.error("🚨 High Risk Detected")
        elif result["probability"] > 0.4:
            st.warning("⚠️ Moderate Risk")
        else:
            st.success("🟢 Low Risk")

    else:
        # fallback logic
        score = (high * 4) + (moderate * 2) + low
        prob = min(score / 12, 1.0)

        st.metric("📊 Risk Score (Offline)", score)
        st.metric("🔮 Probability (Offline)", round(prob, 2))

# -----------------------------
# TREND ANALYSIS
# -----------------------------
st.subheader("📈 Trend Intelligence")

if "score" in df.columns and len(df) > 1:
    diff = df["score"].iloc[-1] - df["score"].iloc[-2]

    if diff > 0:
        st.warning("📈 Increasing Risk Trend")
    elif diff < 0:
        st.info("📉 Decreasing Risk Trend")
    else:
        st.success("➡️ Stable Trend")
else:
    st.info("Not enough data for trend analysis")

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Data Sources ]
      ↓
[ Optional FastAPI Backend ]
      ↓
[ ML Prediction Engine ]
      ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Stable Global Health Intelligence System — Production Ready Design")
