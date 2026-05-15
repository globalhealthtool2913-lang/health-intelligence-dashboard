import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-15 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-15 Global Health Intelligence Platform")
st.caption("Clean visualization layer (backend-ready architecture)")

# -----------------------------
# SIDEBAR
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.sidebar.info("RW-15 frontend is connected to external intelligence pipeline (simulated).")

# -----------------------------
# SIMULATED RECEIVED DATA (FROM BACKEND)
# -----------------------------
def load_data():

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
        },
        {
            "event": "Conflict disrupting healthcare",
            "country": "Sudan",
            "source": "UNICEF",
            "score": 5,
            "risk": "MODERATE",
            "timestamp": datetime.now()
        }
    ])

df = load_data()
df = df[df["country"] == country]

# -----------------------------
# METRICS
# -----------------------------
high = (df["risk"] == "HIGH").sum()
moderate = (df["risk"] == "MODERATE").sum()
low = (df["risk"] == "LOW").sum()

c1, c2, c3 = st.columns(3)
c1.metric("🔴 High", high)
c2.metric("🟠 Moderate", moderate)
c3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT ENGINE (DISPLAY ONLY)
# -----------------------------
score = df["score"].sum()

if score >= 8:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

elif score >= 5:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")

elif score >= 2:
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
# SYSTEM STATUS
# -----------------------------
st.subheader("⚙️ System Status")

st.write(f"""
- Country: **{country}**
- Alert Level: **{alert}**
- Events Loaded: **{len(df)}**
- Last Update: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
""")

# -----------------------------
# ARCHITECTURE VIEW
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Backend Ingestion Layer ]
        ↓
[ Intelligence Engine ]
        ↓
[ Database Storage ]
        ↓
[ Streamlit Visualization Layer ]
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-15 - Clean Frontend Layer for Global Health Intelligence System")
