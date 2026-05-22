import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
from datetime import datetime

# =========================
# STREAMLIT CONFIG
# =========================

st.set_page_config(
    page_title="WHO AI Enterprise System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# 🧠 "MICROSERVICES SIMULATION LAYER"
# =========================

class EventBus:
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)

    def consume(self):
        return self.events[-50:]

bus = EventBus()

# =========================
# 🌍 LIVE DATA INGESTION SERVICE
# =========================

countries = [
    "Ethiopia", "Kenya", "Nigeria",
    "India", "Brazil", "USA",
    "Egypt", "South Africa"
]

def ingestion_service():

    event = {
        "country": random.choice(countries),
        "cases": random.randint(100, 10000),
        "deaths": random.randint(1, 500),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

    bus.publish(event)
    return event

# =========================
# 🧠 AI EPIDEMIOLOGY SERVICE (FREE)
# =========================

def ai_service(event):

    score = event["cases"] * 0.6 + event["deaths"] * 3

    if score > 6000:
        risk = "CRITICAL"
        action = "Emergency WHO response"
    elif score > 3000:
        risk = "HIGH"
        action = "Increase surveillance"
    elif score > 1500:
        risk = "MODERATE"
        action = "Monitor closely"
    else:
        risk = "LOW"
        action = "Routine monitoring"

    return {
        **event,
        "risk": risk,
        "score": score,
        "action": action
    }

# =========================
# 📈 PREDICTION SERVICE
# =========================

def prediction_service(score):

    if score > 6000:
        return "OUTBREAK LIKELY"
    elif score > 3000:
        return "SPREADING"
    else:
        return "STABLE"

# =========================
# 🔔 ALERT SERVICE
# =========================

def alert_service(event):

    if event["risk"] in ["CRITICAL", "HIGH"]:
        return f"🚨 ALERT: {event['country']} is {event['risk']} risk"
    return None

# =========================
# UI HEADER
# =========================

st.title("🌍 WHO AI Enterprise Intelligence System (FREE VERSION)")

# =========================
# CONTROL PANEL
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("System", "ACTIVE")

with col2:
    st.metric("AI Engine", "FREE MODE")

with col3:
    st.metric("Microservices", "SIMULATED")

# =========================
# LIVE PIPELINE RUN
# =========================

st.subheader("🔄 Live Global Event Stream")

if "data" not in st.session_state:
    st.session_state.data = []

# generate new event
new_event = ingestion_service()
processed = ai_service(new_event)

st.session_state.data.append(processed)

# =========================
# DATA FRAME
# =========================

df = pd.DataFrame(st.session_state.data)

if df.empty:
    st.warning("Waiting for global events...")
    st.stop()

# =========================
# 🌍 GLOBAL MAP
# =========================

st.subheader("🌍 Global Surveillance Map")

coords = {
    "Ethiopia": [9.03, 38.74],
    "Kenya": [-1.29, 36.82],
    "Nigeria": [9.08, 8.67],
    "India": [20.59, 78.96],
    "Brazil": [-14.23, -51.92],
    "USA": [37.09, -95.71],
    "Egypt": [26.82, 30.80],
    "South Africa": [-30.56, 22.94]
}

df["lat"] = df["country"].apply(lambda x: coords.get(x, [0,0])[0])
df["lon"] = df["country"].apply(lambda x: coords.get(x, [0,0])[1])

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    size="cases",
    color="risk",
    hover_name="country",
    title="WHO Global Intelligence Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 🔔 ALERT SYSTEM
# =========================

st.subheader("🔔 Smart Alerts")

for item in df.tail(10).to_dict("records"):

    alert = alert_service(item)

    if alert:
        st.error(alert)
    else:
        st.info(f"{item['country']} | {item['risk']}")

# =========================
# 🧠 AI ANALYSIS PANEL
# =========================

st.subheader("🧠 WHO AI Epidemiology Engine")

latest = df.iloc[-1]

st.info(f"""
🌍 Country: {latest['country']}
📊 Cases: {latest['cases']}
⚰️ Deaths: {latest['deaths']}
🚨 Risk: {latest['risk']}
📡 Score: {latest['score']}
📌 Action: {latest['action']}
🕒 Time: {latest['timestamp']}
""")

# =========================
# 📈 PREDICTION ENGINE
# =========================

st.subheader("📈 Prediction Engine")

df["prediction"] = df["score"].apply(prediction_service)

st.dataframe(df)

# =========================
# 🔄 REAL-TIME STREAM SIMULATION
# =========================

st.subheader("🔄 Live Stream (Kafka-style)")

placeholder = st.empty()

for item in df.tail(5).to_dict("records"):

    with placeholder.container():
        st.write(
            f"🌍 {item['country']} | "
            f"Cases: {item['cases']} | "
            f"Deaths: {item['deaths']} | "
            f"Risk: {item['risk']} | "
            f"Time: {item['timestamp']}"
        )

    time.sleep(0.5)

# =========================
# AUTO REFRESH
# =========================

time.sleep(3)
st.rerun()
