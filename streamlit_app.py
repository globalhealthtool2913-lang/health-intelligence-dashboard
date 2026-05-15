import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence System",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard")
st.caption("AI-assisted surveillance + ML-ready architecture")

# -----------------------------
# API CONFIG (CHANGE THIS WHEN DEPLOYING)
# -----------------------------
API_EVENTS = "http://localhost:8000/events"
API_PREDICT = "http://localhost:8000/predict"

# -----------------------------
# SAFE API CALL FUNCTION
# -----------------------------
def safe_get(url):
    try:
        r = requests.get(url, timeout=4)
        return r.json()
    except:
        return None

def safe_post(url, payload):
    try:
        r = requests.post(url, json=payload, timeout=4)
        return r.json()
    except:
        return None

# -----------------------------
# LOAD DATA
# -----------------------------
data = safe_get(API_EVENTS)

if data:
    df = pd.DataFrame(data)
    backend_status = "🟢 Connected"
else:
    df = pd.DataFrame()
    backend_status = "🔴 Offline (Mock Mode)"

# -----------------------------
# STATUS BAR
# -----------------------------
st.subheader("⚙️ System Status")
st.write(f"Backend: {backend_status}")

# -----------------------------
# MOCK DATA IF BACKEND IS OFF
# -----------------------------
if df.empty:
    df = pd.DataFrame([
        {"country": "Ethiopia", "risk": "HIGH", "score": 8},
        {"country": "Kenya", "risk": "MODERATE", "score": 5},
        {"country": "Uganda", "risk": "LOW", "score": 2},
    ])

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
st.subheader("🧠 ML Prediction Engine")

if st.button("Run Prediction"):

    result = safe_post(API_PREDICT, {
        "high": int(high),
        "moderate": int(moderate),
        "low": int(low)
    })

    if result:
        st.metric("📊 Risk Score", round(result.get("risk_score", 0), 2))
        st.metric("🔮 Probability", round(result.get("probability", 0), 2))
    else:
        # fallback logic so UI never breaks
        score = (high * 4) + (moderate * 2) + low
        prob = min(score / 12, 1.0)

        st.metric("📊 Risk Score (Offline)", score)
        st.metric("🔮 Probability (Offline)", round(prob, 2))

# -----------------------------
# TREND ANALYSIS (SAFE)
# -----------------------------
st.subheader("📈 Trend Intelligence")

if len(df) > 1:
    scores = df["score"].tolist() if "score" in df.columns else [0, 1]

    if len(scores) >= 2:
        change = scores[-1] - scores[-2]

        if change > 0:
            st.warning("📈 Increasing Risk Trend")
        elif change < 0:
            st.info("📉 Decreasing Risk Trend")
        else:
            st.success("➡️ Stable Trend")

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# ARCHITECTURE VIEW
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Data Sources ]
      ↓
[ FastAPI Backend (optional) ]
      ↓
[ ML Engine ]
      ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Stable Global Health Intelligence System (Offline + Online Mode Supported)")
