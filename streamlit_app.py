import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px
import os

# =========================
# CONFIG
# =========================

API_BASE = "https://Globalhealthtool.pythonanywhere.com"

st.set_page_config(
    page_title="WHO AI Enterprise System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# SAFE DATA FETCH
# =========================

def fetch_data():

    try:
        r = requests.get(f"{API_BASE}/events", timeout=10)
        data = r.json()

        if isinstance(data, list):
            return data
        return []

    except:
        return []

# =========================
# GPT MEDICAL ANALYST (FIXED + PRODUCTION SAFE)
# =========================

def gpt_analysis(event):

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        prompt = f"""
        WHO Epidemiology Intelligence Report:

        Country: {event.get('country')}
        Cases: {event.get('cases')}
        Deaths: {event.get('deaths')}

        Provide:
        - Risk level
        - Transmission explanation
        - Public health recommendation
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return res.choices[0].message.content

    except:
        return "🧠 GPT unavailable (check API key or connection)"

# =========================
# RISK PREDICTION ENGINE
# =========================

def risk_model(cases, deaths):

    try:
        score = float(cases) * 0.6 + float(deaths) * 3

        if score > 6000:
            return "CRITICAL"
        elif score > 3000:
            return "HIGH"
        elif score > 1500:
            return "MODERATE"
        else:
            return "LOW"

    except:
        return "UNKNOWN"

# =========================
# TELEGRAM ALERT SYSTEM
# =========================

def send_alert(message):

    try:
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        CHAT_ID = os.environ.get("CHAT_ID")

        if not BOT_TOKEN or not CHAT_ID:
            return

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })

    except:
        pass

# =========================
# DATA
# =========================

data = fetch_data()

if data:
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(columns=["country", "cases", "deaths"])

# =========================
# TITLE
# =========================

st.title("🌍 WHO AI Enterprise Intelligence System")

# =========================
# DASHBOARD METRICS
# =========================

st.subheader("📊 Global Intelligence Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", len(df))
col2.metric("System Status", "ACTIVE")
col3.metric("AI Engine", "GPT-ENABLED")

# =========================
# MAP
# =========================

st.subheader("🌍 Global Surveillance Map")

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
        title="WHO Global Risk Map (Enterprise)"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# RISK ENGINE + ALERT SYSTEM
# =========================

st.subheader("🔔 Smart Alert System")

for _, row in df.iterrows():

    risk = risk_model(row["cases"], row["deaths"])

    if risk == "CRITICAL":
        st.error(f"🚨 {row['country']} | Cases: {row['cases']} | Deaths: {row['deaths']}")
        send_alert(f"WHO ALERT: {row['country']} CRITICAL outbreak")

    elif risk == "HIGH":
        st.warning(f"⚠️ {row['country']} | HIGH RISK")

    else:
        st.info(f"{row['country']} | {risk}")

# =========================
# GPT ANALYST
# =========================

st.subheader("🧠 GPT Medical Analyst")

if not df.empty:

    latest = df.iloc[-1].to_dict()

    st.info(gpt_analysis(latest))

# =========================
# PREDICTION ENGINE
# =========================

st.subheader("📈 Prediction Engine")

if not df.empty:

    df["risk_score"] = df.apply(
        lambda r: risk_model(r["cases"], r["deaths"]),
        axis=1
    )

    st.dataframe(df)

# =========================
# REAL-TIME STREAM (SIMULATION)
# =========================

st.subheader("🔄 Real-Time Streaming Engine")

placeholder = st.empty()

for _, row in df.tail(10).iterrows():

    risk = risk_model(row["cases"], row["deaths"])

    with placeholder.container():

        st.write(
            f"🌍 {row['country']} | "
            f"Cases: {row['cases']} | "
            f"Deaths: {row['deaths']} | "
            f"Risk: {risk}"
        )

    time.sleep(0.5)

# =========================
# AUTO REFRESH
# =========================

time.sleep(10)
st.rerun()
