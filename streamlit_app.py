
import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Multi-Source Health Intelligence", layout="wide")

st.title("🌍 Multi-Source Global Health Intelligence System")
st.caption("Stable fusion of GDELT + OWID with ML engine")

# -----------------------------
# SOURCE 1: GDELT
# -----------------------------
def get_gdelt():
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": "health OR outbreak OR epidemic OR virus OR disease",
        "mode": "ArtList",
        "format": "json"
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        data = r.json()

        articles = data.get("articles", [])

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
def get_owid():
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
# LOAD DATA
# -----------------------------
gdelt = get_gdelt()
owid = get_owid()

combined = pd.concat([gdelt, owid], ignore_index=True)

if combined.empty:
    st.error("❌ No data available from any source")
    st.stop()

# -----------------------------
# CLEAN DATA FOR ML
# -----------------------------
combined["signal"] = pd.to_numeric(combined["signal"], errors="coerce")
combined = combined.dropna(subset=["signal"])

# -----------------------------
# ML MODEL
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

col1, col2 = st.columns(2)
col1.metric("Total Signals", len(combined))
col2.metric("Alerts", (combined["anomaly"] == -1).sum())

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(combined)

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Global Trend")

if combined["signal"].mean() > combined["signal"].median():
    st.error("🚨 Increasing global activity detected")
else:
    st.success("🟢 Stable global activity")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT API ]
      ↓
[ OWID Dataset ]
      ↓
[ Data Standardization Layer ]
      ↓
[ ML Risk Engine ]
      ↓
[ Streamlit Dashboard ]
""")

st.caption("Production-safe multi-source intelligence system")
        
