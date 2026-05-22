import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px
import numpy as np
from openai import OpenAI

# =========================
# CONFIG
# =========================

API_BASE = "https://Globalhealthtool.pythonanywhere.com"

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

client = OpenAI(api_key=OPENAI_API_KEY)

# Telegram (optional alerts)
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

st.set_page_config(
    page_title="WHO AI Global Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# GPT MEDICAL ANALYST
# =========================

def gpt_analysis(country, cases, deaths):

    prompt = f"""
    You are a WHO epidemiologist.

    Analyze outbreak:
    Country: {country}
    Cases: {cases}
    Deaths: {deaths}

    Provide:
    - Risk level
    - Transmission pattern
    - Public health recommendation
    """

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except:

        return "AI analysis unavailable"

# =========================
# TELEGRAM ALERT SYSTEM
# =========================

def send_alert(msg):

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

    except:
        pass

# =========================
# FETCH BACKEND DATA
# =========================

def fetch_data():

    try:
        return requests.get(f"{API_BASE}/events").json()
    except:
        return []

# =========================
# PREDICTION MODEL (RISK ENGINE)
# =========================

def predict_risk(cases, deaths):

    score = (cases * 0.6) + (deaths * 3)

    if score > 5000:
        return "CRITICAL"
    elif score > 2500:
        return "HIGH"
    elif score > 1000:
        return "MODERATE"
    else:
        return "LOW"

# =========================
# STREAMING ENGINE
# =========================

def stream_engine(df):

    st.subheader("🔄 Real-Time Intelligence Stream")

    if df.empty:
        st.warning("No data available")
        return

    for _, row in df.tail(10).iterrows():

        risk = predict_risk(row["cases"], row["deaths"])

        if risk == "CRITICAL":

            send_alert(
                f"🚨 WHO ALERT\n{row['country']}\nCases: {row['cases']}\nDeaths: {row['deaths']}"
            )

        st.warning(
            f"{row['country']} | Cases: {row['cases']} | Deaths: {row['deaths']} | Risk: {risk}"
        )

# =========================
# MAIN APP
# =========================

st.title("🌍 WHO AI Global Intelligence System")

data = fetch_data()
df = pd.DataFrame(data) if data else pd.DataFrame()

# =========================
# GLOBAL METRICS
# =========================

st.subheader("📊 Global Intelligence Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Signals", len(df))

if not df.empty:
    col2.metric("Latest Country", df.iloc[-1]["country"])
    col3.metric("Max Cases", df["cases"].max())
else:
    col2.metric("Latest Country", "N/A")
    col3.metric("Max Cases", 0)

# =========================
# 🌍 GLOBAL MAP
# =========================

st.subheader("🌍 Global Risk Map")

if not df.empty:

    coords = {
        "Ethiopia": [9.03, 38.74],
        "Kenya": [-1.29, 36.82],
        "Nigeria": [9.08, 8.67],
        "India": [20.59, 78.96],
        "Brazil": [-14.23, -51.92]
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
        title="WHO Global Surveillance Map"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🧠 GPT MEDICAL ANALYST
# =========================

st.subheader("🧠 GPT Medical Analyst")

if not df.empty:

    latest = df.iloc[-1]

    analysis = gpt_analysis(
        latest["country"],
        latest["cases"],
        latest["deaths"]
    )

    st.info(analysis)

# =========================
# 📈 PREDICTION ENGINE
# =========================

st.subheader("📈 Outbreak Prediction Engine")

if not df.empty:

    df["risk_score"] = df.apply(
        lambda r: (r["cases"] * 0.6) + (r["deaths"] * 3),
        axis=1
    )

    df["risk_level"] = df.apply(
        lambda r: predict_risk(r["cases"], r["deaths"]),
        axis=1
    )

    st.dataframe(df)

# =========================
# 🔄 STREAM ENGINE
# =========================

stream_engine(df)

# =========================
# AUTO REFRESH
# =========================

time.sleep(10)
st.rerun()
