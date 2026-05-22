import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="WHO AI System",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 WHO AI Intelligence System")

# =========================
# TELEGRAM (SAFE)
# =========================

try:
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    TELEGRAM_TOKEN = None
    CHAT_ID = None

def send_alert(msg):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        }, timeout=5)
    except:
        pass

# =========================
# DATA (SAFE SIMULATION)
# =========================

df = pd.DataFrame([
    {"country": "Ethiopia", "cases": 2983, "deaths": 68, "risk": "LOW"},
    {"country": "India", "cases": 5230, "deaths": 112, "risk": "HIGH"},
    {"country": "Brazil", "cases": 7120, "deaths": 201, "risk": "HIGH"},
    {"country": "Kenya", "cases": 1200, "deaths": 30, "risk": "LOW"},
    {"country": "USA", "cases": 8450, "deaths": 310, "risk": "HIGH"}
])

# =========================
# DASHBOARD METRICS
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(df))
col2.metric("System Status", "ACTIVE")
col3.metric("AI Engine", "READY")

st.divider()

# =========================
# TABLE
# =========================

st.subheader("🌍 Global Surveillance Dashboard")
st.dataframe(df, use_container_width=True)

st.divider()

# =========================
# RISK ANALYSIS
# =========================

st.subheader("🚨 Risk Intelligence")

risk_counts = df["risk"].value_counts().reset_index()
risk_counts.columns = ["Risk", "Count"]

col1, col2 = st.columns(2)

with col1:
    st.dataframe(risk_counts)

with col2:
    st.bar_chart(risk_counts.set_index("Risk"))

st.divider()

# =========================
# AI ENGINE
# =========================

st.subheader("🧠 AI Epidemiology Engine")

latest = df.iloc[-1]

st.markdown(f"""
### 🌍 Country: {latest['country']}
📊 Cases: **{latest['cases']}**  
⚰️ Deaths: **{latest['deaths']}**  
🚨 Risk: **{latest['risk']}**
""")

st.divider()

# =========================
# HEATMAP
# =========================

st.subheader("🌍 Global Heatmap")

df["lat"] = np.random.uniform(-60, 80, len(df))
df["lon"] = np.random.uniform(-120, 120, len(df))

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    color="risk",
    size="cases",
    hover_name="country"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# LIVE STREAM
# =========================

st.subheader("🔄 Live Stream")

for _, row in df.iterrows():

    st.write(
        f"🌍 {row['country']} | "
        f"📊 {row['cases']} | "
        f"⚰️ {row['deaths']} | "
        f"🚨 {row['risk']}"
    )

# =========================
# TELEGRAM ALERTS (HIGH RISK ONLY)
# =========================

for _, row in df.iterrows():

    if row["risk"] == "HIGH":

        send_alert(
            f"🚨 WHO ALERT\n"
            f"🌍 {row['country']}\n"
            f"📊 Cases: {row['cases']}\n"
            f"⚰️ Deaths: {row['deaths']}"
        )
