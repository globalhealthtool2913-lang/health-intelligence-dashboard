import streamlit as st
import pandas as pd
import numpy as np
import requests
import pydeck as pdk
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="WHO-Level Global Intelligence System", layout="wide")

st.title("🌍 WHO-Level Global Health Intelligence System")
st.caption("Global outbreak risk monitoring + ML-driven intelligence layer")

# -----------------------------
# SOURCE 1: GDELT
# -----------------------------
def load_gdelt():
    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "health OR outbreak OR epidemic OR virus OR disease",
            "mode": "ArtList",
            "format": "json"
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        articles = data.get("articles", [])

        return pd.DataFrame([{
            "country": a.get("sourceCountry", "Unknown"),
            "signal": 1
        } for a in articles])

    except:
        return pd.DataFrame()

# -----------------------------
# SOURCE 2: OWID
# -----------------------------
def load_owid():
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url, low_memory=False)

        df = df[["location", "total_cases"]].dropna()
        df = df.rename(columns={"location": "country", "total_cases": "signal"})

        return df.groupby("country").tail(1)

    except:
        return pd.DataFrame()

# -----------------------------
# LOAD DATA
# -----------------------------
gdelt = load_gdelt()
owid = load_owid()

frames = []
if not gdelt.empty:
    frames.append(gdelt)
if not owid.empty:
    frames.append(owid)

if len(frames) == 0:
    st.warning("⚠️ No live data available — showing system baseline mode")

    df = pd.DataFrame({
        "country": ["Global"],
        "signal": [1]
    })
else:
    df = pd.concat(frames, ignore_index=True)

# -----------------------------
# CLEAN DATA
# -----------------------------
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# -----------------------------
# COUNTRY AGGREGATION
# -----------------------------
country_df = df.groupby("country")["signal"].sum().reset_index()

# -----------------------------
# RISK SCORING (WHO-STYLE INDEX)
# -----------------------------
max_signal = country_df["signal"].max()
country_df["risk_score"] = (country_df["signal"] / max_signal) * 100

# -----------------------------
# ML ANOMALY DETECTION
# -----------------------------
if len(country_df) > 5:
    model = IsolationForest(contamination=0.2, random_state=42)
    country_df["anomaly"] = model.fit_predict(country_df[["risk_score"]])

    country_df["status"] = country_df["anomaly"].apply(
        lambda x: "🚨 HIGH RISK" if x == -1 else "🟢 NORMAL"
    )
else:
    country_df["status"] = "🟡 INSUFFICIENT DATA"

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Global Risk Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(country_df))
col2.metric("High Risk", (country_df["status"] == "🚨 HIGH RISK").sum())
col3.metric("Avg Risk Score", round(country_df["risk_score"].mean(), 2))

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Country Intelligence Feed")
st.dataframe(country_df, use_container_width=True)

# -----------------------------
# SIMPLE GLOBAL TREND
# -----------------------------
st.subheader("📈 Global Trend Signal")

if country_df["risk_score"].mean() > 50:
    st.error("🚨 Elevated global health risk detected")
else:
    st.success("🟢 Global situation stable")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT News Data ]
        ↓
[ OWID Health Dataset ]
        ↓
[ Country Aggregation Layer ]
        ↓
[ WHO-Style Risk Index (0–100) ]
        ↓
[ ML Anomaly Detection (Isolation Forest) ]
        ↓
[ Streamlit Intelligence Dashboard ]
""")

st.caption("WHO-level global intelligence simulation system")
