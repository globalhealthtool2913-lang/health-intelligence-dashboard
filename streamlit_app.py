import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-18 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-18 Live Global Health Intelligence System")
st.caption("Real-time dashboard connected to live backend pipeline")

# -----------------------------
# BACKEND API
# -----------------------------
API_URL = "http://localhost:8000/events"

# -----------------------------
# FETCH DATA
# -----------------------------
def fetch_data():

    try:
        res = requests.get(API_URL, timeout=5)
        data = res.json()

        if not data:
            return pd.DataFrame()

        return pd.DataFrame(data)

    except:
        st.error("❌ Backend not reachable. Start FastAPI ingestion service.")
        return pd.DataFrame()

df = fetch_data()

# -----------------------------
# FILTERING
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
    high, moderate, low = 0, 0, 0

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT DISPLAY (NO LOGIC HERE)
# -----------------------------
if not df.empty and "score" in df.columns:

    total_score = df["score"].sum()

    if total_score >= 8:
        st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

    elif total_score >= 5:
        st.warning("⚠️ ELEVATED RISK")

    elif total_score >= 2:
        st.info("🔎 WATCH STATUS")

    else:
        st.success("🟢 STABLE CONDITIONS")

else:
    st.info("No active intelligence signals.")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")

if df.empty:
    st.warning("No data available from backend.")
else:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# SYSTEM STATUS
# -----------------------------
st.subheader("⚙️ System Status")

st.write(f"""
- System: **RW-18 Live Intelligence Pipeline**
- Backend: **FastAPI (required)**
- Data Source: **Live ingestion service**
- Country View: **{country}**
""")

# -----------------------------
# ARCHITECTURE VIEW
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Live External Data Sources ]
            ↓
[ Ingestion Service (FastAPI Worker) ]
            ↓
[ Intelligence Engine + Scoring ]
            ↓
[ Database (PostgreSQL / SQLite) ]
            ↓
[ API Layer ]
            ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-18 - Live Global Health Intelligence Dashboard (Frontend Only)")
