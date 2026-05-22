import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# CONFIG
# =========================

API_BASE = "https://Globalhealthtool.pythonanywhere.com"

st.set_page_config(
    page_title="WHO AI Global Surveillance System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🌍 WHO AI Global Surveillance System")
st.markdown("Real-Time WHO + GDELT + AI Epidemiology Intelligence")

# =========================
# FETCH DATA
# =========================

def get_data():
    try:
        return requests.get(f"{API_BASE}/events").json()
    except:
        return []

def get_diseases():
    try:
        return requests.get(f"{API_BASE}/diseases").json()
    except:
        return {}

data = get_data()
disease_data = get_diseases()

df = pd.DataFrame(data) if data else pd.DataFrame()

# =========================
# GLOBAL STATUS
# =========================

st.subheader("🛰️ Global Surveillance Status")

col1, col2, col3 = st.columns(3)

col1.metric("Active Signals", len(df))
col2.metric("Last Update", str(datetime.now().strftime("%H:%M:%S")))
col3.metric("Data Sources", "WHO + GDELT")

# =========================
# DISEASE BREAKDOWN
# =========================

st.subheader("🧬 Disease Intelligence Breakdown")

if disease_data:

    st.json(disease_data)

# =========================
# GLOBAL MAP (SIMULATED SURVEILLANCE)
# =========================

st.subheader("🌍 Global Surveillance Map")

if not df.empty:

    country_coords = {
        "Ethiopia": [9.03, 38.74],
        "Kenya": [-1.29, 36.82],
        "Nigeria": [9.08, 8.67],
        "India": [20.59, 78.96],
        "Brazil": [-14.23, -51.92]
    }

    df["lat"] = df["country"].apply(lambda x: country_coords.get(x, [0,0])[0])
    df["lon"] = df["country"].apply(lambda x: country_coords.get(x, [0,0])[1])

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size="cases" if "cases" in df.columns else None,
        hover_name="country",
        title="WHO Global Risk Map"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🔔 MOBILE ALERT SYSTEM
# =========================

st.subheader("🔔 Mobile Alert System")

if not df.empty:

    alerts = df[df["cases"] > 2500]

    if not alerts.empty:

        for _, row in alerts.iterrows():

            st.error(
                f"🚨 ALERT: {row['country']} | "
                f"Cases: {row['cases']} | "
                f"Deaths: {row['deaths']}"
            )
    else:
        st.success("No critical alerts detected")

# =========================
# 🧠 GPT MEDICAL ANALYST (SIMULATED AI REASONING)
# =========================

st.subheader("🧠 GPT Medical Analyst")

if not df.empty:

    latest = df.iloc[-1]

    cases = latest.get("cases", 0)
    deaths = latest.get("deaths", 0)

    mortality = round((deaths / cases) * 100, 2) if cases else 0

    if cases > 4000:
        spread = "Very High Transmission"
    elif cases > 2000:
        spread = "Moderate Transmission"
    else:
        spread = "Controlled Transmission"

    if mortality > 5:
        severity = "Severe"
    elif mortality > 2:
        severity = "Moderate"
    else:
        severity = "Low"

    st.info(f"""
### 🧠 AI Epidemiology Report

Country: {latest.get('country')}

Transmission: {spread}

Severity: {severity}

Mortality Rate: {mortality}%

### AI Interpretation:
The outbreak in {latest.get('country')} shows {spread.lower()} with {severity.lower()} severity.
Immediate surveillance and regional coordination recommended.

This analysis is generated from WHO + GDELT intelligence streams.
""")

# =========================
# 🌐 GLOBAL SURVEILLANCE FEED
# =========================

st.subheader("🌐 Global Surveillance Feed")

if not df.empty:

    for _, row in df.tail(10).iterrows():

        st.warning(
            f"🌍 {row['country']} | "
            f"Cases: {row['cases']} | "
            f"Deaths: {row['deaths']}"
        )

# =========================
# 📊 RAW DATA VIEW
# =========================

st.subheader("📊 Raw Intelligence Data")

st.dataframe(df)

# =========================
# AUTO REFRESH
# =========================

st.caption("Auto-refresh every 10 seconds")

st.rerun()
