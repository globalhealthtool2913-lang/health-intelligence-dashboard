import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="WHO Enterprise Intelligence System", layout="wide")

st.title("🌍 WHO-Level Global Health Intelligence System (Enterprise)")
st.caption("Single-file production system with database + ML + multi-source fusion")

# -----------------------------
# DATABASE (AUTO CREATE)
# -----------------------------
DB = "who_system.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    df = pd.read_sql("SELECT * FROM signals", conn)
    conn.close()
    return df

init_db()

# -----------------------------
# DATA SOURCE 1: GDELT
# -----------------------------
def get_gdelt():
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

# -----------------------------
# DATA SOURCE 2: OWID
# -----------------------------
def get_owid():
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url, low_memory=False)

        df = df[["location", "total_cases"]].dropna()
        df = df.rename(columns={"location": "country", "total_cases": "signal"})
        df["source"] = "OWID"

        return df.groupby("country").tail(1)

    except:
        return pd.DataFrame()

# -----------------------------
# INGEST DATA (LIVE + STORE)
# -----------------------------
gdelt = get_gdelt()
owid = get_owid()

frames = []

if not gdelt.empty:
    frames.append(gdelt)
if not owid.empty:
    frames.append(owid)

if len(frames) > 0:
    new_data = pd.concat(frames, ignore_index=True)
    save(new_data)

# -----------------------------
# LOAD FROM DATABASE (PRIMARY)
# -----------------------------
df = load()

# -----------------------------
# SAFE FALLBACK (NO CRASH)
# -----------------------------
if df.empty:
    st.warning("⚠️ No stored intelligence data yet — showing system baseline mode")

    df = pd.DataFrame({
        "country": ["Global"],
        "signal": [1],
        "source": ["SYSTEM"]
    })

# -----------------------------
# CLEAN
# -----------------------------
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# -----------------------------
# AGGREGATION
# -----------------------------
country_df = df.groupby("country")["signal"].sum().reset_index()

# -----------------------------
# RISK INDEX (WHO STYLE)
# -----------------------------
country_df["risk_score"] = (
    country_df["signal"] / country_df["signal"].max()
) * 100

# -----------------------------
# ML ENGINE
# -----------------------------
if len(country_df) >= 5:
    model = IsolationForest(contamination=0.2, random_state=42)
    country_df["anomaly"] = model.fit_predict(country_df[["risk_score"]])

    country_df["status"] = country_df["anomaly"].apply(
        lambda x: "🚨 HIGH RISK" if x == -1 else "🟢 NORMAL"
    )
else:
    country_df["status"] = "🟡 LOW DATA"

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Global Intelligence Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(country_df))
col2.metric("High Risk", (country_df["status"] == "🚨 HIGH RISK").sum())
col3.metric("Avg Risk Score", round(country_df["risk_score"].mean(), 2))

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(country_df, use_container_width=True)

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Global Trend")

if country_df["risk_score"].mean() > 50:
    st.error("🚨 Elevated global health risk detected")
else:
    st.success("🟢 Global situation stable")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Live APIs: GDELT + OWID ]
        ↓
[ Auto Ingestion Layer ]
        ↓
[ SQLite Persistent Storage ]
        ↓
[ Aggregation + Feature Engineering ]
        ↓
[ ML Risk Engine (Isolation Forest) ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption("Enterprise WHO-style global intelligence system (single-file production)")
