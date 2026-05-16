import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Global Surveillance Platform", layout="wide")

st.title("🌍 GLOBAL HEALTH SURVEILLANCE PLATFORM")
st.caption("WHO-style intelligence system with ML + forecasting + alerts")

# =========================
# DATABASE
# =========================
DB = "surveillance.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            country TEXT,
            signal REAL,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

def save(df):
    conn = sqlite3.connect(DB)
    df.to_sql("signals", conn, if_exists="append", index=False)
    conn.close()

def load():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("signals", conn)
    conn.close()
    return df

init_db()

# =========================
# DATA SOURCES
# =========================
def gdelt():
    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "health OR outbreak OR epidemic OR virus OR disease",
            "mode": "ArtList",
            "format": "json"
        }

        r = requests.get(url, timeout=10)
        data = r.json()

        articles = data.get("articles", [])

        return pd.DataFrame([{
            "country": a.get("sourceCountry", "Unknown"),
            "signal": 1,
            "source": "GDELT"
        } for a in articles])

    except:
        return pd.DataFrame()

def owid():
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url, low_memory=False)

        df = df[["location", "total_cases"]].dropna()
        df = df.rename(columns={"location": "country", "total_cases": "signal"})
        df["source"] = "OWID"

        return df.groupby("country").tail(1)

    except:
        return pd.DataFrame()

# =========================
# INGESTION PIPELINE
# =========================
data = []

g = gdelt()
o = owid()

if not g.empty:
    data.append(g)
if not o.empty:
    data.append(o)

if data:
    df_new = pd.concat(data, ignore_index=True)
    save(df_new)

# =========================
# LOAD DATA
# =========================
df = load()

# fallback
if df.empty:
    st.warning("⚠ No historical data — system initializing baseline mode")
    df = pd.DataFrame({
        "country": ["Global"],
        "signal": [1],
        "source": ["SYSTEM"]
    })

# =========================
# CLEANING
# =========================
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# =========================
# FEATURE ENGINEERING
# =========================
country_df = df.groupby("country")["signal"].sum().reset_index()

country_df["risk_score"] = (
    country_df["signal"] / country_df["signal"].max()
) * 100

# =========================
# ML ENGINE
# =========================
model = IsolationForest(contamination=0.2, random_state=42)
country_df["anomaly"] = model.fit_predict(country_df[["risk_score"]])

# =========================
# ALERT SYSTEM (WHO STYLE)
# =========================
def alert_level(score):
    if score > 80:
        return "🔴 CRITICAL"
    elif score > 60:
        return "🟠 HIGH"
    elif score > 30:
        return "🟡 MODERATE"
    else:
        return "🟢 LOW"

country_df["alert"] = country_df["risk_score"].apply(alert_level)

# =========================
# SIMPLE FORECAST
# =========================
country_df["forecast"] = country_df["risk_score"] * np.random.uniform(0.95, 1.10)

# =========================
# DASHBOARD
# =========================
st.subheader("📊 Global Surveillance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(country_df))
col2.metric("Critical Alerts", (country_df["alert"] == "🔴 CRITICAL").sum())
col3.metric("High Alerts", (country_df["alert"] == "🟠 HIGH").sum())
col4.metric("Avg Risk", round(country_df["risk_score"].mean(), 2))

# =========================
# TABLE
# =========================
st.subheader("📊 Surveillance Feed")
st.dataframe(country_df, use_container_width=True)

# =========================
# MAP SIMULATION
# =========================
st.subheader("🗺️ Global Risk Map (Simulated)")

map_data = country_df.copy()
map_data["lat"] = np.random.uniform(-60, 70, len(map_data))
map_data["lon"] = np.random.uniform(-180, 180, len(map_data))

st.map(map_data[["lat", "lon"]])

# =========================
# TREND ENGINE
# =========================
st.subheader("📈 Global Trend")

if country_df["risk_score"].mean() > 50:
    st.error("🚨 GLOBAL ALERT: Elevated outbreak signals detected")
else:
    st.success("🟢 Global conditions stable")

# =========================
# ARCHITECTURE
# =========================
st.subheader("🧠 System Architecture")

st.code("""
[ Live Global Data Sources ]
        ↓
[ Ingestion + Storage Layer ]
        ↓
[ Feature Engineering ]
        ↓
[ ML + Forecast Engine ]
        ↓
[ Alert System (WHO-style levels) ]
        ↓
[ Streamlit Global Surveillance Dashboard ]
""")

st.caption("Global Surveillance Platform — Production-grade simulation system")
