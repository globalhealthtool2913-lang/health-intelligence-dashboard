import streamlit as st
import requests
import pandas as pd
import time

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="WHO AI Enterprise Dashboard",
    page_icon="🌍",
    layout="wide"
)

API_GATEWAY = "http://localhost:8000/pipeline"

# =========================================
# HEADER
# =========================================

st.title("🌍 WHO AI Enterprise Intelligence System")
st.caption("Microservices Architecture (FastAPI + Streamlit)")

# =========================================
# LOAD DATA FROM MICROSERVICE BACKEND
# =========================================

def load_data():

    try:
        response = requests.get(API_GATEWAY, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    except:
        return []

data = load_data()

# =========================================
# SAFETY CHECK
# =========================================

if not data:
    st.warning("Backend not running or no data available.")
    st.stop()

df = pd.DataFrame(data)

# =========================================
# METRICS
# =========================================

col1, col2, col3 = st.columns(3)

col1.metric("Events", len(df))
col2.metric("System", "ACTIVE")
col3.metric("Architecture", "MICROSERVICES")

# =========================================
# GLOBAL VIEW
# =========================================

st.subheader("🌍 Global Surveillance Dashboard")

st.dataframe(df)

# =========================================
# RISK ANALYSIS
# =========================================

st.subheader("🚨 Risk Analysis")

if "risk" in df.columns:

    risk_counts = df["risk"].value_counts()

    st.bar_chart(risk_counts)

# =========================================
# PREDICTION VIEW
# =========================================

st.subheader("📈 Prediction Output")

if "prediction" in df.columns:

    st.dataframe(df[["country", "risk", "prediction", "score"]])

# =========================================
# GLOBAL STREAM (REAL-TIME SIMULATION)
# =========================================

st.subheader("🔄 Live Stream")

placeholder = st.empty()

for i in range(len(df)):

    item = df.iloc[i]

    with placeholder.container():

        st.write(
            f"🌍 {item['country']} | "
            f"Cases: {item['cases']} | "
            f"Deaths: {item['deaths']} | "
            f"Risk: {item['risk']} | "
            f"Prediction: {item.get('prediction','N/A')}"
        )

    time.sleep(0.3)

# =========================================
# AUTO REFRESH
# =========================================

time.sleep(5)
st.rerun()
