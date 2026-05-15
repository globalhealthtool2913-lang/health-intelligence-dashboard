import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-16 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-16 Global Health Intelligence Platform")
st.caption("Production-ready frontend (connected to backend architecture)")

# -----------------------------
# SIDEBAR
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.sidebar.info("This UI is designed to connect to a live backend API (RW-17+).")

# -----------------------------
# SIMULATED BACKEND RESPONSE (PLACEHOLDER)
# -----------------------------
def fetch_from_backend():

    return pd.DataFrame([
        {
            "event": "Cholera outbreak reported",
            "country": "Ethiopia",
            "source": "WHO",
            "score": 8,
            "risk": "HIGH",
            "timestamp": datetime.now()
        },
        {
            "event": "Flood affecting hospitals",
            "country": "Kenya",
            "source": "ReliefWeb",
            "score": 4,
            "risk": "MODERATE",
            "timestamp": datetime.now()
        }
    ])

df = fetch_from_backend()
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
# ALERT ENGINE (DISPLAY ONLY)
# -----------------------------
total_score = df["score"].sum()

if total_score >= 8:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

elif total_score >= 5:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")

elif total_score >= 2:
    alert = "WATCH"
    st.info("🔎 WATCH STATUS")

else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# SYSTEM ARCHITECTURE VIEW
# -----------------------------
st.subheader("🧠 System Architecture (RW-16 Design)")

st.code("""
[ Data Sources (WHO / GDELT / APIs) ]
                ↓
        [ Backend API Layer ]
                ↓
        [ Intelligence Engine ]
                ↓
        [ Database (PostgreSQL) ]
                ↓
        [ Streamlit Frontend ]
""")

# -----------------------------
# BACKEND INTEGRATION PLACEHOLDER
# -----------------------------
st.subheader("🔌 Backend Integration Status")

st.write("""
- Backend API: **NOT CONNECTED (placeholder mode)**
- Data Source: **Simulated**
- Next Step: Connect FastAPI + Live Data Ingestion
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-16 - Clean Production Frontend for Global Health Intelligence System")
