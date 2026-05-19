import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import feedparser
from datetime import datetime
from sklearn.ensemble import IsolationForest

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="WHO Global Intelligence System",
    layout="wide"
)

st.title("🌍 WHO Global Intelligence System")
st.caption("Multi-source Health Intelligence + AI Risk + Forecasting")

# =========================
# DATA SOURCE (LIVE + FALLBACK)
# =========================
@st.cache_data(ttl=120)
def load_data():
    try:
        url = "https://disease.sh/v3/covid-19/countries"
        r = requests.get(url, timeout=10)
        data = r.json()

        df = pd.DataFrame(data)[[
            "country",
            "casesPerOneMillion",
            "deathsPerOneMillion"
        ]]

        df.columns = ["Country", "Cases", "Deaths"]
        df["Policy"] = np.random.randint(40, 90, len(df))

        return df, True

    except:
        return pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        }), False

df, live = load_data()

if live:
    st.success("🟢 LIVE DATA ACTIVE")
else:
    st.warning("🔴 Fallback Mode")

# =========================
# CLEAN DATA
# =========================
df = df.dropna()

# =========================
# RISK ENGINE
# =========================
df["Risk"] = (
    df["Cases"] * 0.4 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.2
)

df["Risk"] = df["Risk"].clip(0, 5000)

# =========================
# AI ANOMALY DETECTION
# =========================
model = IsolationForest(contamination=0.1, random_state=42)
df["Anomaly"] = model.fit_predict(df[["Risk"]])
df["Anomaly"] = df["Anomaly"].apply(lambda x: "ALERT" if x == -1 else "OK")

# =========================
# FORECASTING (SAFE SIMPLE MODEL)
# =========================
df["Forecast"] = df["Risk"].rolling(2).mean().fillna(df["Risk"])

# =========================
# FILTERS
# =========================
st
