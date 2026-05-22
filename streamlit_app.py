import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# =========================
# CONFIG
# =========================

API_BASE = "https://Globalhealthtool.pythonanywhere.com"

st.set_page_config(
    page_title="WHO AI Global System (Free)",
    page_icon="🌍",
    layout="wide"
)

# =========================
# FETCH DATA (SAFE)
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
# FREE WHO AI ENGINE (NO OPENAI)
# =========================

def who_ai_analysis(event):

    country = event.get("country", "Unknown")
    cases = float(event.get("cases", 0))
    deaths = float(event.get("deaths", 0))

    score = cases * 0.6 + deaths * 3

    if score > 5000:
        risk = "CRITICAL"
        action = "Emergency WHO response required"
    elif score > 3000:
        risk = "HIGH"
        action = "Increase surveillance and contact tracing"
    elif score > 1500:
        risk = "MODERATE"
        action = "Monitor and prepare health resources"
    else:
        risk = "LOW"
        action = "Routine monitoring"

    if deaths > cases * 0.1:
        transmission = "Severe outbreak pattern"
    else:
        transmission = "Community transmission"

    return {
        "country": country,
        "cases": cases,
        "deaths": deaths,
        "risk": risk,
        "transmission": transmission,
        "recommendation": action,
        "score": score
    }

# =========================
# LOAD DATA
# =========================

data = fetch_data()

if data:
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(columns=["country", "cases", "deaths"])

# =========================
# TITLE
# =========================

st.title("🌍 WHO AI Global Intelligence System (FREE VERSION)")

# =========================
# DASHBOARD
# =========================

st.subheader("📊 Global Intelligence Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Events", len(df))
col2.metric("System", "ACTIVE")
col3.metric("AI Engine", "FREE MODE")

# =========================
# SAFETY CHECK
# =========================

if df.empty:
    st.warning("No data available from backend")

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
        title="WHO Global Surveillance Map (FREE AI)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # ALERT SYSTEM
    # =========================

    st.subheader("🔔 Smart Alerts")

    for _, row in df.iterrows():

        result = who_ai_analysis(row)

        if result["risk"] == "CRITICAL":
            st.error(f"🚨 {result['country']} | Cases: {result['cases']} | Deaths: {result['deaths']}")
        elif result["risk"] == "HIGH":
            st.warning(f"⚠️ {result['country']} | HIGH RISK")
        else:
            st.info(f"{result['country']} | {result['risk']}")

    # =========================
    # AI ANALYSIS PANEL
    # =========================

    st.subheader("🧠 WHO AI Epidemiology Engine (FREE)")

    latest = df.iloc[-1]

    analysis = who_ai_analysis(latest)

    st.info(f"""
    🌍 Country: {analysis['country']}
    📊 Cases: {analysis['cases']}
    ⚰️ Deaths: {analysis['deaths']}
    🚨 Risk: {analysis['risk']}
    📡 Transmission: {analysis['transmission']}
    📌 Recommendation: {analysis['recommendation']}
    """)

    # =========================
    # PREDICTION TABLE
    # =========================

    st.subheader("📈 Prediction Engine")

    predictions = []

    for _, row in df.iterrows():
        predictions.append(who_ai_analysis(row))

    pred_df = pd.DataFrame(predictions)

    st.dataframe(pred_df)

    # =========================
    # REAL-TIME STREAM SIMULATION
    # =========================

    st.subheader("🔄 Real-Time Stream")

    placeholder = st.empty()

    for _, row in df.tail(10).iterrows():

        result = who_ai_analysis(row)

        with placeholder.container():
            st.write(
                f"🌍 {result['country']} | "
                f"Cases: {result['cases']} | "
                f"Deaths: {result['deaths']} | "
                f"Risk: {result['risk']}"
            )

        time.sleep(0.5)

# =========================
# AUTO REFRESH
# =========================

time.sleep(10)
st.rerun()
