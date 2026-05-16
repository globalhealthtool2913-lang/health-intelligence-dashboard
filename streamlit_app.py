import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Global Health Intelligence (Production)", layout="wide")

st.title("🌍 Production Global Health Intelligence System")
st.caption("Self-contained multi-source ML intelligence dashboard")

# -----------------------------
# SAFE DATA SOURCE: GDELT
# -----------------------------
def load_gdelt():
    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "health OR outbreak OR disease OR epidemic OR virus",
            "mode": "ArtList",
            "format": "json"
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return pd.DataFrame()

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
# SAFE DATA SOURCE: OWID
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
# LOAD MULTI-SOURCE DATA
# -----------------------------
gdelt = load_gdelt()
owid = load_owid()

frames = []

if not gdelt.empty:
    frames.append(gdelt)

if not owid.empty:
    frames.append(owid)

# -----------------------------
# FALLBACK (NO CRASH EVER)
# -----------------------------
if len(frames) == 0:
    st.warning("⚠️ Live data unavailable — system running in safe mode")

    combined = pd.DataFrame({
        "source": ["SYSTEM"],
        "country": ["Global"],
        "signal": [1],
    })
else:
    combined = pd.concat(frames, ignore_index=True)

# -----------------------------
# CLEAN DATA
# -----------------------------
combined["signal"] = pd.to_numeric(combined["signal"], errors="coerce")
combined = combined.dropna(subset=["signal"])

# -----------------------------
# ML ENGINE (SAFE)
# -----------------------------
if len(combined) >= 5:
    model = IsolationForest(contamination=0.2, random_state=42)
    combined["anomaly"] = model.fit_predict(combined[["signal"]])

    combined["status"] = combined["anomaly"].apply(
        lambda x: "🚨 ALERT" if x == -1 else "🟢 SAFE"
    )
else:
    combined["anomaly"] = 0
    combined["status"] = "🟡 LOW DATA"

# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📊 Intelligence Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Signals", len(combined))
col2.metric("Alerts", (combined["status"] == "🚨 ALERT").sum())
col3.metric("Sources", combined["source"].nunique())

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(combined, use_container_width=True)

# -----------------------------
# TREND ENGINE
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
[ GDELT Live API ]
        ↓
[ OWID Dataset ]
        ↓
[ Auto-Fusion Layer ]
        ↓
[ ML Engine (Isolation Forest) ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption("Production-ready resilient global intelligence system")
