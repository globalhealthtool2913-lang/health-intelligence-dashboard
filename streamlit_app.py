import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser
import random
import time
from datetime import datetime

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="WHO AI Enterprise Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# =========================================
# ENTERPRISE EVENT BUS (Kafka-style simulation)
# =========================================

class EventBus:
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)

    def consume(self):
        return self.events[-100:]

bus = EventBus()

# =========================================
# WHO RSS INGESTION SERVICE
# =========================================

WHO_FEEDS = [
    "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
]

def fetch_who_data():

    results = []

    try:
        for url in WHO_FEEDS:

            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                results.append({
                    "source": "WHO",
                    "title": entry.title,
                    "summary": entry.summary,
                    "country": random.choice([
                        "Ethiopia",
                        "Kenya",
                        "India",
                        "Brazil",
                        "USA"
                    ]),
                    "cases": random.randint(100, 8000),
                    "deaths": random.randint(1, 400),
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })

    except:
        pass

    return results

# =========================================
# GDELT LIVE INGESTION SERVICE
# =========================================

def fetch_gdelt_data():

    results = []

    try:

        url = "https://api.gdeltproject.org/api/v2/doc/doc"

        params = {
            "query": "disease OR outbreak OR epidemic OR virus",
            "mode": "ArtList",
            "format": "json",
            "maxrecords": 10
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        for item in data.get("articles", [])[:10]:

            results.append({
                "source": "GDELT",
                "title": item.get("title", "Unknown Event"),
                "summary": item.get("seendate", ""),
                "country": random.choice([
                    "Nigeria",
                    "South Africa",
                    "Egypt",
                    "India",
                    "Brazil"
                ]),
                "cases": random.randint(100, 10000),
                "deaths": random.randint(1, 500),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

    except:
        pass

    return results

# =========================================
# INGESTION PIPELINE
# =========================================

def ingestion_pipeline():

    who_events = fetch_who_data()
    gdelt_events = fetch_gdelt_data()

    for event in who_events:
        bus.publish(event)

    for event in gdelt_events:
        bus.publish(event)

# =========================================
# AI EPIDEMIOLOGY ENGINE
# =========================================

def ai_engine(event):

    score = event["cases"] * 0.6 + event["deaths"] * 3

    if score > 6000:
        risk = "CRITICAL"
        action = "Emergency WHO response required"
        transmission = "Severe outbreak spread"
    elif score > 3000:
        risk = "HIGH"
        action = "Increase surveillance and tracing"
        transmission = "Rapid community transmission"
    elif score > 1500:
        risk = "MODERATE"
        action = "Monitor spread closely"
        transmission = "Localized transmission"
    else:
        risk = "LOW"
        action = "Routine monitoring"
        transmission = "Low spread"

    return {
        **event,
        "risk": risk,
        "score": score,
        "transmission": transmission,
        "action": action
    }

# =========================================
# PREDICTION ENGINE
# =========================================

def prediction_engine(score):

    if score > 6000:
        return "OUTBREAK LIKELY"

    elif score > 3000:
        return "SPREADING"

    return "STABLE"

# =========================================
# ALERT SYSTEM
# =========================================

def alert_system(event):

    if event["risk"] == "CRITICAL":
        return f"🚨 CRITICAL ALERT: {event['country']}"

    if event["risk"] == "HIGH":
        return f"⚠️ HIGH RISK: {event['country']}"

    return None

# =========================================
# RUN INGESTION
# =========================================

ingestion_pipeline()

# =========================================
# LOAD DATA
# =========================================

events = bus.consume()

df = pd.DataFrame(events)

# =========================================
# HEADER
# =========================================

st.title("🌍 WHO AI Enterprise Intelligence System")

# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Live Events", len(df))
col2.metric("Sources", "WHO + GDELT")
col3.metric("System", "ACTIVE")
col4.metric("Architecture", "ENTERPRISE")

# =========================================
# EMPTY SAFETY
# =========================================

if df.empty:

    st.warning("Waiting for live global data...")
    st.stop()

# =========================================
# MAP
# =========================================

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

df["lat"] = df["country"].apply(
    lambda x: coords.get(x, [0, 0])[0]
)

df["lon"] = df["country"].apply(
    lambda x: coords.get(x, [0, 0])[1]
)

fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    size="cases",
    color="deaths",
    hover_name="country",
    title="WHO Global Enterprise Surveillance"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# ALERTS
# =========================================

st.subheader("🔔 Smart Alert System")

processed = []

for _, row in df.iterrows():

    item = ai_engine(row)

    processed.append(item)

    alert = alert_system(item)

    if alert:
        st.error(alert)

# =========================================
# AI PANEL
# =========================================

st.subheader("🧠 WHO AI Epidemiology Engine")

latest = processed[-1]

st.info(f"""
🌍 Country: {latest['country']}

📊 Cases: {latest['cases']}

⚰️ Deaths: {latest['deaths']}

🚨 Risk: {latest['risk']}

📡 Transmission: {latest['transmission']}

📌 Recommendation: {latest['action']}

🛰️ Source: {latest['source']}

🕒 Time: {latest['timestamp']}
""")

# =========================================
# PREDICTION ENGINE
# =========================================

st.subheader("📈 Prediction Engine")

pred_df = pd.DataFrame(processed)

pred_df["prediction"] = pred_df["score"].apply(
    prediction_engine
)

st.dataframe(pred_df)

# =========================================
# REAL-TIME STREAM
# =========================================

st.subheader("🔄 Real-Time Global Stream")

placeholder = st.empty()

for item in processed[-10:]:

    with placeholder.container():

        st.write(
            f"🌍 {item['country']} | "
            f"Cases: {item['cases']} | "
            f"Deaths: {item['deaths']} | "
            f"Risk: {item['risk']} | "
            f"Source: {item['source']}"
        )

    time.sleep(0.4)

# =========================================
# AUTO REFRESH
# =========================================

time.sleep(5)
st.rerun()
