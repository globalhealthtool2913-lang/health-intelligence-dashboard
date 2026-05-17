import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
import time
import pydeck as pdk

from datetime import datetime
from sklearn.ensemble import IsolationForest

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="WHO Digital Twin", layout="wide")

st.title("🌍 WHO DIGITAL TWIN SYSTEM")
st.caption("Real-time global health intelligence (resilient production version)")

DB = "who.db"

# =========================
# DATABASE
# =========================
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            country TEXT,
            signal REAL,
            source TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save(df):
    conn = sqlite3.connect(DB)
    df.to_sql("signals", conn, if_exists="append", index=False)
    conn.close()

def load():
    conn = sqlite3.connect(DB)
    try:
        df = pd.read_sql("SELECT * FROM signals", conn)
    except:
        df = pd.DataFrame(columns=["country", "signal", "source", "timestamp"])
    conn.close()
    return df

# =========================
# SAFE API CALL (FIX 429)
# =========================
def safe_request(url, params, retries=3):

    for i in range(retries):
        try:
            r = requests.get(url, params=params, timeout=10)

            if r.status_code == 429:
                time.sleep(2 * (i + 1))
                continue

            if r.status_code != 200:
                return None

            return r.json()

        except:
            time.sleep(1)

    return None

# =========================
# GDELT LIVE DATA
# =========================
def fetch_gdelt():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "health OR outbreak OR epidemic OR virus",
        "mode": "ArtList",
        "format": "json"
    }

    data = safe_request(url, params)

    if not data:
        return pd.DataFrame()

    articles = data.get("articles", [])

    rows = []

    for a in articles:
        rows.append({
            "country": a.get("sourceCountry", "Unknown"),
            "signal": 1,
            "source": "GDELT",
            "timestamp": str(datetime.utcnow())
        })

    return pd.DataFrame(rows)

# =========================
# FALLBACK ONLY IF API FAILS
# =========================
def fallback():

    countries = ["Ethiopia","Kenya","USA","India","Brazil","Germany","China"]

    return pd.DataFrame({
        "country": countries,
        "signal": np.random.randint(10, 300, len(countries)),
        "source": "FALLBACK",
        "timestamp": str(datetime.utcnow())
    })

# =========================
# INGESTION
# =========================
gdelt = fetch_gdelt()

if not gdelt.empty:
    save(gdelt)
else:
    st.warning("⚠️ Live API unavailable — using fallback only")

    save(fallback())

# =========================
# LOAD DATA
# =========================
df = load()

if df.empty:
    st.error("❌ No data available")
    st.stop()

# =========================
# CLEAN
# =========================
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# =========================
# AGGREGATION
# =========================
world = df.groupby("country")["signal"].sum().reset_index()

# =========================
# RISK SCORE
# =========================
world["risk"] = (world["signal"] / world["signal"].max()) * 100

# =========================
# ML MODEL
# =========================
if len(world) > 4:

    model = IsolationForest(contamination=0.2, random_state=42)
    world["anomaly"] = model.fit_predict(world[["risk"]])

    world["status"] = world["anomaly"].apply(
        lambda x: "🚨 OUTBREAK" if x == -1 else "🟢 STABLE"
    )

else:
    world["status"] = "🟡 LOW DATA"

# =========================
# WHO LEVEL
# =========================
def who(x):
    if x > 80: return "🔴 LEVEL 5"
    if x > 60: return "🟠 LEVEL 4"
    if x > 40: return "🟡 LEVEL 3"
    if x > 20: return "🟢 LEVEL 2"
    return "⚪ LEVEL 1"

world["WHO"] = world["risk"].apply(who)

# =========================
# METRICS
# =========================
st.subheader("📊 Intelligence Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Countries", len(world))
c2.metric("Outbreak Zones", (world["status"] == "🚨 OUTBREAK").sum())
c3.metric("Avg Risk", round(world["risk"].mean(), 2))

# =========================
# TABLE
# =========================
st.subheader("📊 Global State")
st.dataframe(world, use_container_width=True)

# =========================
# MAP
# =========================
coords = {
    "Ethiopia":[9.1,40.4],
    "Kenya":[-1.2,36.8],
    "USA":[37,-95],
    "India":[20,78],
    "Brazil":[-14,-51],
    "Germany":[51,10],
    "China":[35,104]
}

world["lat"] = world["country"].apply(lambda x: coords.get(x,[0,0])[0])
world["lon"] = world["country"].apply(lambda x: coords.get(x,[0,0])[1])

st.subheader("🗺️ Global Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=world,
    get_position='[lon, lat]',
    get_radius='risk * 50000',
    get_fill_color='[255,0,0,140]',
    pickable=True
)

view = pdk.ViewState(latitude=20, longitude=0, zoom=1)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

# =========================
# TREND
# =========================
st.subheader("📈 Trend")

if world["risk"].mean() > 60:
    st.error("🚨 High global activity")
else:
    st.success("🟢 Stable global activity")

# =========================
# TOP RISK
# =========================
top = world.sort_values("risk", ascending=False).iloc[0]

st.subheader("🚨 Highest Risk Country")

st.write(top["country"])
st.write("Risk:", round(top["risk"],2))
st.write("Status:", top["WHO"])


    
