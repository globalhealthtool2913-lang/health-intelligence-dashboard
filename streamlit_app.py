import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px
import threading
import random

# =========================
# CONFIG
# =========================

API_BASE = "https://Globalhealthtool.pythonanywhere.com"

# Telegram config (optional)
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

st.set_page_config(
    page_title="WHO AI Global Production System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# GLOBAL STREAM (Kafka-style simulation)
# =========================

stream_data = []

countries = ["Ethiopia", "Kenya", "Nigeria", "India", "Brazil", "USA"]

def data_pipeline():

    while True:

        event = {
            "country": random.choice(countries),
            "cases": random.randint(500, 7000),
            "deaths": random.randint(5, 400),
            "timestamp": time.time()
        }

        stream_data.append(event)

        if len(stream_data) > 100:
            stream_data.pop(0)

        time.sleep(3)

# start pipeline thread
threading.Thread(target=data_pipeline, daemon=True).start()

# =========================
# TELEGRAM ALERT SYSTEM
# =========================

def send_telegram(message):

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })

    except:
        pass

# =========================
# GPT MEDICAL ANALYST (SAFE)
# =========================

def gpt_analysis(event):

    try:
        from openai import OpenAI
        client = OpenAI()

        prompt = f"""
        You are a WHO epidemiologist.

        Analyze:
        Country: {event['country']}
        Cases: {event['cases']}
        Deaths: {event['deaths']}

        Give:
        - Risk level
        - Transmission pattern
        - Action recommendation
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return "AI analysis unavailable"

# =========================
# RISK PREDICTION ENGINE
# =========================

def risk_model(cases, deaths):

    score = cases * 0.7 + deaths * 3

    if score > 6000:
        return "CRITICAL"
    elif score > 3000:
        return "HIGH"
    elif score > 1500:
        return "MODERATE"
    else:
        return "LOW"

# =========================
# FETCH BACKEND DATA
# =========================

def fetch_backend():

    try:
        return requests.get(f"{API_BASE}/events").json()
    except:
        return []

# =========================
# STREAMLIT UI
# =========================

st.title("🌍 WHO AI GLOBAL PRODUCTION SYSTEM")

# combine backend + stream pipeline
backend_data = fetch_backend()
df_backend = pd.DataFrame(backend_data) if backend_data else pd.DataFrame()
df_stream = pd.DataFrame(stream_data) if stream_data else pd.DataFrame()

# =========================
# DASHBOARD METRICS
# =========================

st.subheader("📊 Global Intelligence Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Live Stream Events", len(stream_data))
col2.metric("Backend Records", len(df_backend))
col3.metric("System Status", "ACTIVE")

# =========================
# GLOBAL MAP
# =========================

st.subheader("🌍 Global Surveillance Map")

df = df_stream if not df_stream.empty else df_backend

if not df.empty:

    coords = {
        "Ethiopia": [9.03, 38.74],
        "Kenya": [-1.29, 36.82],
        "Nigeria": [9.08, 8.67],
        "India": [20.59, 78.96],
        "Brazil": [-14.23, -51.92],
        "USA": [37.09, -95.71]
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
        title="WHO Global Risk Map (Production)"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🔔 ALERT SYSTEM
# =========================

st.subheader("🔔 Mobile Alert System")

if not df.empty:

    for _, row in df.tail(10).iterrows():

        risk = risk_model(row["cases"], row["deaths"])

        if risk == "CRITICAL":

            send_telegram(
                f"🚨 WHO ALERT\n{row['country']}\nCases: {row['cases']}\nDeaths: {row['deaths']}"
            )

            st.error(f"{row['country']} - CRITICAL ALERT")

        elif risk == "HIGH":
            st.warning(f"{row['country']} - HIGH RISK")

# =========================
# 🧠 GPT MEDICAL ANALYST
# =========================

st.subheader("🧠 GPT Medical Analyst")

if not df.empty:

    latest = df.iloc[-1]

    analysis = gpt_analysis(latest)

    st.info(analysis)

# =========================
# 📈 PREDICTION ENGINE
# =========================

st.subheader("📈 Prediction Engine")

if not df.empty:

    df["risk_score"] = df.apply(
        lambda r: r["cases"] * 0.7 + r["deaths"] * 3,
        axis=1
    )

    df["risk_level"] = df.apply(
        lambda r: risk_model(r["cases"], r["deaths"]),
        axis=1
    )

    st.dataframe(df)

# =========================
# 🔄 REAL-TIME STREAM VIEW
# =========================

st.subheader("🔄 Real-Time Streaming Engine (Kafka-style)")

placeholder = st.empty()

for i in range(len(stream_data)):

    event = stream_data[i]

    risk = risk_model(event["cases"], event["deaths"])

    with placeholder.container():

        st.write(
            f"🌍 {event['country']} | "
            f"Cases: {event['cases']} | "
            f"Deaths: {event['deaths']} | "
            f"Risk: {risk}"
        )

    time.sleep(0.5)

# =========================
# AUTO REFRESH
# =========================

time.sleep(10)
st.rerun()
