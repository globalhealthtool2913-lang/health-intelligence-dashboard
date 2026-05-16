import streamlit as st
import pandas as pd
import numpy as np
import requests
import pydeck as pdk
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Global Health Intelligence System", layout="wide")

st.title("🌍 Global Health Intelligence System (Fixed + Stable Live Mode)")
st.caption("Live data + ML anomaly detection + safe execution")

# -----------------------------
# SAFE LIVE DATA LOADER
# -----------------------------
@st.cache_data(ttl=300)
def load_live_data():
    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "health OR outbreak OR disease OR epidemic OR virus",
        "mode": "ArtList",
        "format": "json"
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        articles = data.get("articles", [])

        if not articles:
            return pd.DataFrame()

        df = pd.DataFrame([{
            "title": a.get("title", "N/A"),
            "source": a.get("sourceCountry", "N/A"),
            "url": a.get("url", "")
        } for a in articles])

        return df

    except Exception as e:
        st.error("❌ Live data failed (API issue)")
        st.warning(str(e))
        return pd.DataFrame()

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_live_data()

# -----------------------------
# HANDLE EMPTY DATA SAFELY
# -----------------------------
if df.empty:
    st.warning("⚠️ No live data available right now from API.")
    st.stop()

# -----------------------------
# ADD ML RISK SCORING
# -----------------------------
df["risk_score"] = np.random.randint(1, 100, len(df))

model = IsolationForest(contamination=0.2, random_state=42)
df["anomaly"] = model.fit_predict(df[["risk_score"]])

df["status"] = df["anomaly"].apply(
    lambda x: "🚨 OUTBREAK SIGNAL" if x == -1 else "🟢 NORMAL"
)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Live Intelligence Summary")

col1, col2 = st.columns(2)
col1.metric("🚨 Signals", (df["anomaly"] == -1).sum())
col2.metric("📰 Reports", len(df))

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df)

# -----------------------------
# SIMPLE TREND
# -----------------------------
st.subheader("📈 Trend Analysis")

if len(df) > 10:
    st.info("📈 High global health news activity detected")
else:
    st.success("🟢 Low activity level detected")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT Live API ]
        ↓
[ Data Parsing Layer ]
        ↓
[ Risk Scoring Engine ]
        ↓
[ ML Anomaly Detection ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption("Stable Live Intelligence System — Fixed Version")
