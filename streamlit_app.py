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
    page_title="WHO AI Global Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# SAFE DATA FETCH
# =========================

def fetch_data():

    try:
        res = requests.get(f"{API_BASE}/events", timeout=10)
        data = res.json()

        if isinstance(data, list):
            return data
        return []

    except:
        return []

# =========================
# GPT ANALYST (SAFE + FIXED)
# =========================

def gpt_analysis(event):

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        prompt = f"""
        WHO Epidemiology Analysis:

        Country: {event.get('country')}
        Cases: {event.get('cases')}
        Deaths: {event.get('deaths')}

        Provide:
        1. Risk level
        2. Transmission pattern
        3. Recommendation
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return "🧠 AI unavailable (check API key)"

# =========================
# RISK MODEL (FIXED)
# =========================

def risk_model(cases, deaths):

    try:
        score = float(cases) * 0.6 + float(deaths) * 3

        if score > 5000:
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

st.title("🌍 WHO AI Global Intelligence System")

# =========================
# DASHBOARD METRICS
# =========================

st.subheader("📊 Global Intelligence Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Events", len(df))
col2.metric("Status", "ACTIVE")
col3.metric("Backend", "LIVE")

# =========================
# SAFE CHECK
# =========================

if df.empty:

    st.warning("No outbreak data available from backend")

else:

    # =========================
    # MAP
    # =========================

    st.subheader("🌍 Global Surveillance Map")

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
        title="WHO Global Risk Map"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # ALERT SYSTEM
    # =========================

    st.subheader("🔔 Smart Alerts")

    for _, row in df.iterrows():

        risk = risk_model(row["cases"], row["deaths"])

        if risk == "CRITICAL":
            st.error(f"🚨 {row['country']} | Cases: {row['cases']} | Deaths: {row['deaths']}")
        elif risk == "HIGH":
            st.warning(f"⚠️ {row['country']} | Cases: {row['cases']} | Deaths: {row['deaths']}")

    # =========================
    # GPT ANALYST
    # =========================

    st.subheader("🧠 GPT Medical Analyst")

    latest = df.iloc[-1].to_dict()

    st.info(gpt_analysis(latest))

    # =========================
    # PREDICTION ENGINE
    # =========================

    st.subheader("📈 Prediction Engine")

    df["risk_score"] = df.apply(
        lambda r: risk_model(r["cases"], r["deaths"]),
        axis=1
    )

    st.dataframe(df)

    # =========================
    # LIVE FEED
    # =========================

    st.subheader("🔄 Live Stream")

    for _, row in df.tail(10).iterrows():

        st.write(
            f"🌍 {row['country']} | "
            f"Cases: {row['cases']} | "
            f"Deaths: {row['deaths']} | "
            f"Risk: {risk_model(row['cases'], row['deaths'])}"
        )

# =========================
# AUTO REFRESH
# =========================

time.sleep(10)
st.rerun()

