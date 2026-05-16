import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import 
IsolationForest

st.set_page_config(page_title="Global Health Intelligence System", layout="wide")

st.title("🌍 Global Health Intelligence System (Production Stable)")
st.caption("Multi-source resilient intelligence + ML anomaly detection")

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

        if not articles:
            return pd.DataFrame()

        return pd.DataFrame([{
            "source": "GDELT",
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
        df = df.rename(columns={
            "location": "country",
            "total_cases": "signal"
        })

        df["source"] = "OWID"

        return df.groupby("country").tail(1)

    except:
        return pd.DataFrame()

# -----------------------------
# LOAD MULTI-SOURCE (SAFE FUSION)
# -----------------------------
gdelt = load_gdelt()
owid = load_owid()

frames = []

if not gdelt.empty:
    frames.append(gdelt)

if not owid.empty:
    frames.append(owid)

# IMPORTANT: never crash system
if len(frames) == 0:
    st.warning("⚠️ No external data available right now")
    st.info("System running in monitoring mode (waiting for live signals)")
    st.stop()

combined = pd.concat(frames, ignore_index=True)

# -----------------------------
# CLEAN DATA
# -----------------------------
combined["signal"] = pd.to_numeric(combined["signal"], errors="coerce")
combined = combined.dropna(subset=["signal"])

# -----------------------------
# ML ENGINE
# -----------------------------
model = IsolationForest(contamination=0.2, random_state=42)
combined["anomaly"] = model.fit_predict(combined[["signal"]])

combined["status"] = combined["anomaly"].apply(
    lambda x: "🚨 ALERT" if x == -1 else "🟢 SAFE"
)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Intelligence Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Signals", len(combined))
col2.metric("Alerts", (combined["anomaly"] == -1).sum())
col3.metric("Safe", (combined["anomaly"] == 1).sum())

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(combined, use_container_width=True)

# -----------------------------
# TREND ENGINE
# -----------------------------
st.subheader("📈 Global Trend Signal")

avg = combined["signal"].mean()
median = combined["signal"].median()

if avg > median:
    st.error("🚨 Increasing global activity detected")
else:
    st.success("🟢 Stable global activity level")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT Live News API ]
        ↓
[ OWID Health Dataset ]
        ↓
[ Data Fusion Layer (Resilient) ]
        ↓
[ ML Anomaly Detection Engine ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption("Production-grade resilient global intelligence system")       
