import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-17 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-17 Live Global Health Intelligence Dashboard")
st.caption("Frontend-only system connected to FastAPI backend")

# -----------------------------
# BACKEND URL
# -----------------------------
API_URL = "http://localhost:8000/events"

# -----------------------------
# LOAD DATA FROM BACKEND
# -----------------------------
def load_data():

    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()

        if len(data) == 0:
            return pd.DataFrame()

        return pd.DataFrame(data)

    except:
        st.error("❌ Backend not connected. Start FastAPI server.")
        return pd.DataFrame()

df = load_data()

# -----------------------------
# COUNTRY FILTER (IF AVAILABLE)
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
        alert = "CRITICAL"

    elif total_score >= 5:
        st.warning("⚠️ ELEVATED RISK")
        alert = "ELEVATED"

    elif total_score >= 2:
        st.info("🔎 WATCH STATUS")
        alert = "WATCH"

    else:
        st.success("🟢 STABLE CONDITIONS")
        alert = "STABLE"

else:
    alert = "NO DATA"

# -----------------------------
# DATA DISPLAY
# -----------------------------
st.subheader("📊 Intelligence Feed")

if df.empty:
    st.info("No data available from backend.")
else:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# SYSTEM STATUS
# -----------------------------
st.subheader("⚙️ System Status")

st.write(f"""
- Backend: **FastAPI (RW-17)**
- Frontend: **Streamlit**
- Country View: **{country}**
- Alert Level: **{alert}**
""")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ External Data Sources ]
          ↓
[ FastAPI Backend ]
          ↓
[ Intelligence Engine ]
          ↓
[ API Response Layer ]
          ↓
[ Streamlit Dashboard ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-17 - Production Split Architecture (Frontend Only)")
