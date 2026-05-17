import streamlit as st
import requests
import pandas as pd

# ======================================
# CONFIG
# ======================================
st.set_page_config(
    page_title="WHO Global Intelligence System",
    layout="wide"
)

st.title("🏥 WHO GLOBAL HEALTH ALERT SYSTEM")
st.caption("Live production dashboard (Streamlit + FastAPI)")

# ======================================
# IMPORTANT: YOUR RAILWAY BACKEND URL
# ======================================
API_BASE = "https://your-railway-app.up.railway.app"  # 🔴 REPLACE THIS

# ======================================
# LOAD ALERTS
# ======================================
def get_alerts():

    try:
        r = requests.get(f"{API_BASE}/alerts", timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()

        return data.get("alerts", [])

    except:
        return []

# ======================================
# LOAD SIGNALS
# ======================================
def get_signals():

    try:
        r = requests.get(f"{API_BASE}/signals", timeout=10)

        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()

        df = pd.DataFrame(data)

        if df.empty:
            return df

        df.columns = ["country", "signal"]

        return df

    except:
        return pd.DataFrame()

# ======================================
# FETCH DATA
# ======================================
alerts = get_alerts()
df = get_signals()

# ======================================
# ALERT SECTION
# ======================================
st.subheader("🚨 Active Global Alerts")

if len(alerts) == 0:
    st.success("🟢 No active outbreak alerts detected")
else:
    st.error("🚨 ACTIVE OUTBREAK ALERTS")

    st.dataframe(pd.DataFrame(alerts), use_container_width=True)

# ======================================
# GLOBAL INTELLIGENCE
# ======================================
st.subheader("📊 Global Intelligence Overview")

if not df.empty:

    world = df.groupby("country")["signal"].sum().reset_index()

    world["risk"] = (
        world["signal"] / world["signal"].max()
    ) * 100

    c1, c2, c3 = st.columns(3)

    c1.metric("Countries", len(world))
    c2.metric("Signals", len(df))
    c3.metric("Avg Risk", round(world["risk"].mean(), 2))

    st.subheader("🔥 High Risk Countries")

    st.dataframe(
        world.sort_values("risk", ascending=False),
        use_container_width=True
    )

else:
    st.warning("No signal data received from backend")

# ======================================
# SYSTEM STATUS
# ======================================
st.subheader("🧠 System Architecture")

st.code("""
Streamlit Frontend (UI)
        ↓
FastAPI Backend (Railway)
        ↓
Risk Engine
        ↓
Alert System
        ↓
WHO Surveillance Dashboard
""")

st.caption("WHO-style production intelligence system")
