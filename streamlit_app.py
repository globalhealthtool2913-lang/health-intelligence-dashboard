import streamlit as st
import requests
import pandas as pd
import time

# =========================================
# CONFIG (AWS / LOCAL SWITCHABLE)
# =========================================

st.set_page_config(
    page_title="WHO AI Global Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# 👉 CHANGE THIS IN AWS DEPLOYMENT
API_GATEWAY = st.secrets.get(
    "API_GATEWAY",
    "http://localhost:8000/pipeline"
)

# =========================================
# HEADER
# =========================================

st.title("🌍 WHO AI Enterprise Intelligence Platform")
st.caption("Docker + Kafka + Microservices + Cloud Architecture")

# =========================================
# FETCH DATA FROM MICROSERVICE BACKEND
# =========================================

@st.cache_data(ttl=10)
def fetch_data():

    try:
        response = requests.get(API_GATEWAY, timeout=15)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    except:
        return []

data = fetch_data()

# =========================================
# SAFETY CHECK
# =========================================

if not data:

    st.warning("⚠️ Backend not available or Kafka pipeline not streaming.")
    st.stop()

df = pd.DataFrame(data)

# =========================================
# METRICS DASHBOARD
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Live Events", len(df))
col2.metric("Architecture", "AWS + Kafka")
col3.metric("System Status", "ACTIVE")
col4.metric("AI Engine", "ENABLED")

# =========================================
# GLOBAL TABLE
# =========================================

st.subheader("🌍 Global Surveillance Feed")

st.dataframe(df, use_container_width=True)

# =========================================
# RISK VISUALIZATION
# =========================================

st.subheader("🚨 Risk Distribution")

if "risk" in df.columns:

    st.bar_chart(df["risk"].value_counts())

# =========================================
# COUNTRY ANALYSIS
# =========================================

st.subheader("🌍 Country-Level Intelligence")

if "country" in df.columns:

    country_stats = df.groupby("country")[["cases", "deaths"]].sum()

    st.dataframe(country_stats)

# =========================================
# PREDICTION VIEW
# =========================================

st.subheader("📈 AI Prediction Engine Output")

if "prediction" in df.columns:

    st.dataframe(
        df[["country", "cases", "deaths", "risk", "prediction", "score"]]
    )

# =========================================
# LIVE STREAM (KAFKA SIMULATION VIEW)
# =========================================

st.subheader("🔄 Real-Time Global Stream (Kafka Feed Simulation)")

placeholder = st.empty()

for i in range(min(len(df), 10)):

    item = df.iloc[i]

    with placeholder.container():

        st.write(
            f"🌍 **{item.get('country','Unknown')}** | "
            f"📊 Cases: {item.get('cases',0)} | "
            f"⚰️ Deaths: {item.get('deaths',0)} | "
            f"🚨 Risk: {item.get('risk','N/A')} | "
            f"🧠 Prediction: {item.get('prediction','N/A')} | "
            f"📡 Source: {item.get('source','system')}"
        )

    time.sleep(0.2)

# =========================================
# AUTO REFRESH (REAL-TIME SIMULATION)
# =========================================

time.sleep(8)
st.rerun()
