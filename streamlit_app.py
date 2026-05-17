import streamlit as st
import requests
import pandas as pd

# ======================================
# CONFIG
# ======================================
st.set_page_config(
    page_title="WHO Global Alert System",
    layout="wide"
)

st.title("🏥 WHO GLOBAL HEALTH ALERT SYSTEM")
st.caption("Production surveillance dashboard (FastAPI + AI Engine)")

# ======================================
# BACKEND
# ======================================
API_BASE = "http://localhost:8000"

# ======================================
# FETCH ALERTS
# ======================================
def load_alerts():

    try:
        r = requests.get(f"{API_BASE}/alerts", timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()

        return data.get("alerts", [])

    except:
        return []

# ======================================
# FETCH SIGNALS
# ======================================
def load_signals():

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
# LOAD DATA
# ======================================
alerts = load_alerts()
df = load_signals()

# ======================================
# ALERT SECTION
# ======================================
st.subheader("🚨 Active Global Alerts")

if len(alerts) == 0:
    st.success("🟢 No active outbreak alerts detected")
else:
    st.error("🚨 HIGH RISK ALERTS ACTIVE")

    alert_df = pd.DataFrame(alerts)

    st.dataframe(alert_df, use_container_width=True)

# ======================================
# GLOBAL OVERVIEW
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

    # TOP RISKS
    st.subheader("🔥 High Risk Countries")

    st.dataframe(
        world.sort_values("risk", ascending=False),
        use_container_width=True
    )

else:
    st.warning("No signal data available")

# ======================================
# SYSTEM STATUS
# ======================================
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT Live Data ]
        ↓
[ FastAPI Risk Engine ]
        ↓
[ AI Alert System ]
        ↓
[ PostgreSQL / DB Layer ]
        ↓
[ Streamlit WHO Dashboard ]
""")

# ======================================
# FOOTER
# ======================================
st.caption("WHO-style production surveillance system (alert-enabled)")
