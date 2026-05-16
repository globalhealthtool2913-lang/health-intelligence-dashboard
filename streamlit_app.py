
   import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from sklearn.ensemble import IsolationForest
from datetime import datetime

st.set_page_config(page_title="WHO Digital Twin System", layout="wide")

st.title("🌍 WHO DIGITAL TWIN SYSTEM")
st.caption("Simulated global health intelligence model (real-world fusion + ML + forecasting)")

# =========================
# DATABASE (DIGITAL TWIN MEMORY)
# =========================
DB = "digital_twin.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS world_state (
            country TEXT,
            signal REAL,
            source TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save(df):
    conn = sqlite3.connect(DB)
    df.to_sql("world_state", conn, if_exists="append", index=False)
    conn.close()

def load():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM world_state", conn)
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
            "source": "GDELT",
            "timestamp": str(datetime.utcnow())
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
        df["timestamp"] = str(datetime.utcnow())

        return df.groupby("country").tail(1)

    except:
        return pd.DataFrame()

# =========================
# SYNTHETIC GLOBAL SIGNALS (DIGITAL TWIN CORE)
# =========================
def synthetic_world_state():
    countries = ["Ethiopia", "Kenya", "USA", "India", "Brazil"]

    return pd.DataFrame({
        "country": countries,
        "signal": np.random.randint(10, 500, len(countries)),
        "source": "SYNTHETIC_TWIN",
        "timestamp": str(datetime.utcnow())
    })

# =========================
# FUSION LAYER
# =========================
data = [gdelt(), owid(), synthetic_world_state()]
df_new = pd.concat([d for d in data if not d.empty], ignore_index=True)

save(df_new)

# =========================
# LOAD WORLD STATE
# =========================
df = load()

if df.empty:
    st.warning("🌍 Digital twin initializing world state...")
    df = synthetic_world_state()

# =========================
# CLEAN
# =========================
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# =========================
# WORLD STATE ENGINE
# =========================
world = df.groupby("country")["signal"].sum().reset_index()

world["risk_score"] = (
    world["signal"] / world["signal"].max()
) * 100

# =========================
# ML ENGINE (TWIN BRAIN)
# =========================
model = IsolationForest(contamination=0.2, random_state=42)
world["anomaly"] = model.fit_predict(world[["risk_score"]])

world["status"] = world["anomaly"].apply(
    lambda x: "🚨 OUTBREAK ZONE" if x == -1 else "🟢 STABLE ZONE"
)

# =========================
# WHO ALERT SYSTEM
# =========================
def who_level(score):
    if score > 80:
        return "🔴 LEVEL 5 - CRITICAL"
    elif score > 60:
        return "🟠 LEVEL 4 - HIGH"
    elif score > 40:
        return "🟡 LEVEL 3 - MODERATE"
    elif score > 20:
        return "🟢 LEVEL 2 - LOW"
    else:
        return "🟢 LEVEL 1 - MINIMAL"

world["WHO_ALERT"] = world["risk_score"].apply(who_level)

# =========================
# DASHBOARD
# =========================
st.subheader("🌍 Digital World State")

col1, col2, col3 = st.columns(3)

col1.metric("Countries", len(world))
col2.metric("Outbreak Zones", (world["status"] == "🚨 OUTBREAK ZONE").sum())
col3.metric("Avg Risk", round(world["risk_score"].mean(), 2))

st.dataframe(world, use_container_width=True)

# =========================
# GLOBAL TREND
# =========================
st.subheader("📈 Global Trend Engine")

if world["risk_score"].mean() > 50:
    st.error("🚨 DIGITAL TWIN ALERT: Elevated global health instability detected")
else:
    st.success("🟢 Global system stable (digital twin simulation)")

# =========================
# ARCHITECTURE
# =========================
st.subheader("🧠 Digital Twin Architecture")

st.code("""
[ Real + Synthetic Global Data ]
        ↓
[ Fusion Layer (World State Builder) ]
        ↓
[ Digital Twin Memory (SQLite) ]
        ↓
[ ML Brain (Risk + Anomaly Detection) ]
        ↓
[ WHO Alert System (Level 1–5) ]
        ↓
[ Streamlit Visualization Layer ]
""")

st.caption("WHO Digital Twin System — simulated global health intelligence model") 
