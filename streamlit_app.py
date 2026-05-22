import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import threading
import random

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="WHO AI Enterprise Live System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# LIVE GLOBAL DATA PIPELINE (SIMULATED WHO + GDELT)
# =========================

live_stream = []

countries = [
    "Ethiopia", "Kenya", "Nigeria",
    "India", "Brazil", "USA",
    "South Africa", "Egypt"
]

def live_ingestion_pipeline():

    while True:

        event = {
            "country": random.choice(countries),
            "cases": random.randint(100, 9000),
            "deaths": random.randint(1, 600),
            "source": random.choice(["WHO", "GDELT", "RSS"])
        }

        live_stream.append(event)

        # keep memory light
        if len(live_stream) > 200:
            live_stream.pop(0)

        time.sleep(2)

# start pipeline
threading.Thread(target=live_ingestion_pipeline, daemon=True).start()

# =========================
# ENTERPRISE RISK ENGINE
# =========================

def risk_engine(cases, deaths):

    score = cases * 0.6 + deaths * 3

    if score > 6000:
        return "CRITICAL"
    elif score > 3000:
        return "HIGH"
    elif score > 1500:
        return "MODERATE"
    else:
        return "LOW"

# =========================
# AI WHO REASONING (FREE)
# =========================

def who_ai(event):

    risk = risk_engine(event["cases"], event["deaths"])

    if risk == "CRITICAL":
        action = "Emergency response required"
        transmission = "High severity outbreak"
    elif risk == "HIGH":
        action = "Increase surveillance"
        transmission = "Rapid community spread"
    elif risk == "MODERATE":
        action = "Monitor situation"
        transmission = "Localized transmission"
    else:
        action = "Routine monitoring"
        transmission = "Low spread risk"

    return {
        "country": event["country"],
        "cases": event["cases"],
        "deaths": event["deaths"],
        "source": event["source"],
        "risk": risk,
        "transmission": transmission,
        "action": action
    }

# =========================
# STREAMLIT UI
# =========================

st.title("🌍 WHO AI Enterprise Live Intelligence System")

# =========================
# METRICS
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("Live Events", len(live_stream))
col2.metric("Data Sources", "WHO + GDELT + RSS")
col3.metric("System", "ENTERPRISE ACTIVE")

# =========================
# DATA FRAME
# =========================

df = pd.DataFrame(live_stream)

if df.empty:
    st.warning("Waiting for live global data stream...")
    st.stop()

# =========================
# GLOBAL MAP
# =========================

st.subheader("🌍 Live Global Surveillance Map")

coords = {
    "Ethiopia": [9.03, 38.74],
    "Kenya": [-1.29, 36.82],
    "Nigeria": [9.08, 8.67],
    "India": [20.59, 78.96],
    "Brazil": [-14.23, -51.92],
    "USA": [37.09, -95.71],
    "South Africa": [-30.56, 22.94],
    "Egypt": [26.82, 30.80]
}

df["lat"] = df["country"].apply(lambda x: coords.get(x, [0,0])[0])
df["lon"] = df["country"].apply(lambda x: coords.get(x, [0,0])[1])

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    size="cases",
    color="deaths",
    hover_name="country",
    title="WHO Global Live Surveillance (Enterprise Mode)"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# ALERT SYSTEM
# =========================

st.subheader("🔔 Smart Alert System")

for _, row in df.tail(15).iterrows():

    result = who_ai(row)

    if result["risk"] == "CRITICAL":
        st.error(f"🚨 {result['country']} | CRITICAL OUTBREAK")
    elif result["risk"] == "HIGH":
        st.warning(f"⚠️ {result['country']} | HIGH RISK")
    else:
        st.info(f"{result['country']} | {result['risk']}")

# =========================
# AI ANALYSIS PANEL
# =========================

st.subheader("🧠 WHO AI Epidemiology Engine")

latest = df.iloc[-1]

analysis = who_ai(latest)

st.info(f"""
🌍 Country: {analysis['country']}
📊 Cases: {analysis['cases']}
⚰️ Deaths: {analysis['deaths']}
📡 Source: {analysis['source']}
🚨 Risk: {analysis['risk']}
🦠 Transmission: {analysis['transmission']}
📌 Action: {analysis['action']}
""")

# =========================
# PREDICTION ENGINE
# =========================

st.subheader("📈 Prediction Engine")

df["risk_level"] = df.apply(
    lambda r: risk_engine(r["cases"], r["deaths"]),
    axis=1
)

df["risk_score"] = df.apply(
    lambda r: r["cases"] * 0.6 + r["deaths"] * 3,
    axis=1
)

st.dataframe(df.tail(50))

# =========================
# REAL-TIME STREAM VIEW
# =========================

st.subheader("🔄 Real-Time Global Stream")

placeholder = st.empty()

for event in live_stream[-10:]:

    result = who_ai(event)

    with placeholder.container():
        st.write(
            f"🌍 {result['country']} | "
            f"Cases: {result['cases']} | "
            f"Deaths: {result['deaths']} | "
            f"Source: {result['source']} | "
            f"Risk: {result['risk']}"
        )

    time.sleep(0.5)

# =========================
# AUTO REFRESH
# =========================

time.sleep(5)
st.rerun()
