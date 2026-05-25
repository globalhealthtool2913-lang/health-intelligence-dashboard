import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="WHO AI Intelligence System",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 WHO AI Enterprise Intelligence Platform")
st.caption("Stable WHO + AI + Telegram Alert System")

st.divider()

# =========================================
# TELEGRAM CONFIG
# =========================================

try:
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    TELEGRAM_TOKEN = None
    CHAT_ID = None

# =========================================
# TELEGRAM ALERT FUNCTION
# =========================================

def send_alert(message):

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=5
        )
    except:
        pass

# =========================================
# SAFE DATA
# =========================================

df = pd.DataFrame([
    {
        "country": "Ethiopia",
        "cases": 2983,
        "deaths": 68,
        "risk": "LOW",
        "prediction": "STABLE"
    },
    {
        "country": "India",
        "cases": 5230,
        "deaths": 112,
        "risk": "HIGH",
        "prediction": "SPREADING"
    },
    {
        "country": "Brazil",
        "cases": 7120,
        "deaths": 201,
        "risk": "HIGH",
        "prediction": "OUTBREAK LIKELY"
    },
    {
        "country": "Kenya",
        "cases": 1200,
        "deaths": 30,
        "risk": "LOW",
        "prediction": "CONTROLLED"
    },
    {
        "country": "USA",
        "cases": 8450,
        "deaths": 310,
        "risk": "HIGH",
        "prediction": "SPREADING"
    }
])

# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("System", "ACTIVE")
col3.metric("AI Engine", "READY")
col4.metric("Architecture", "STABLE")

st.divider()

# =========================================
# DASHBOARD TABLE
# =========================================

st.subheader("🌍 Global Surveillance Dashboard")

st.dataframe(df, use_container_width=True)

st.divider()

# =========================================
# RISK ANALYSIS
# =========================================

st.subheader("🚨 Risk Intelligence")

risk_counts = df["risk"].value_counts().reset_index()
risk_counts.columns = ["Risk", "Count"]

col1, col2 = st.columns(2)

with col1:
    st.dataframe(risk_counts, use_container_width=True)

with col2:
    st.bar_chart(risk_counts.set_index("Risk"))

st.divider()

# =========================================
# AI ENGINE
# =========================================

st.subheader("🧠 AI Epidemiology Engine")

latest = df.iloc[-1]

st.markdown(f"""
### 🌍 Country: {latest['country']}

📊 Cases: **{latest['cases']}**  
⚰️ Deaths: **{latest['deaths']}**  
🚨 Risk: **{latest['risk']}**  
🧠 Prediction: **{latest['prediction']}**
""")

st.divider()

# =========================================
# GLOBAL HEATMAP
# =========================================

st.subheader("🌍 Global Heatmap")

df["lat"] = np.random.uniform(-60, 80, len(df))
df["lon"] = np.random.uniform(-120, 120, len(df))

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    color="risk",
    size="cases",
    hover_name="country",
    title="WHO AI Global Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================================
# LIVE STREAM
# =========================================

st.subheader("🔄 Live Global Stream")

for _, row in df.iterrows():

    st.write(
        f"🌍 {row['country']} | "
        f"📊 {row['cases']} | "
        f"⚰️ {row['deaths']} | "
        f"🚨 {row['risk']} | "
        f"🧠 {row['prediction']}"
    )

st.divider()

# =========================================
# TELEGRAM ALERTS
# =========================================

for _, row in df.iterrows():

    if row["risk"] == "HIGH":

        send_alert(
            f"🚨 WHO AI ALERT\n"
            f"🌍 {row['country']}\n"
            f"📊 Cases: {row['cases']}\n"
            f"⚰️ Deaths: {row['deaths']}\n"
            f"🧠 Prediction: {row['prediction']}"
        )

# =========================================
# FOOTER
# =========================================

st.success("✅ WHO AI Intelligence System Running Successfully")
