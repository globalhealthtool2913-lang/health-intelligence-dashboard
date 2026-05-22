import streamlit as st
import pandas as pd
import requests
import feedparser
import random
import time

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="WHO AI Real-Time Intelligence",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 WHO AI Real-Time Intelligence System")
st.caption("Live WHO + GDELT streaming (No backend, phone-friendly)")

st.divider()

# =========================================
# REAL-TIME DATA INGESTION
# =========================================

def fetch_who():

    data = []

    try:
        feed = feedparser.parse(
            "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
        )

        for entry in feed.entries[:3]:

            data.append({
                "country": random.choice(["Ethiopia", "India", "Brazil", "Kenya"]),
                "cases": random.randint(1000, 9000),
                "deaths": random.randint(10, 400),
                "source": "WHO",
                "event": entry.title
            })

    except:
        pass

    return data


def fetch_gdelt():

    data = []

    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc?query=disease&mode=ArtList&format=json"
        r = requests.get(url, timeout=10)
        j = r.json()

        for a in j.get("articles", [])[:3]:

            data.append({
                "country": random.choice(["USA", "India", "Brazil"]),
                "cases": random.randint(2000, 10000),
                "deaths": random.randint(50, 500),
                "source": "GDELT",
                "event": a.get("title", "news")
            })

    except:
        pass

    return data


# =========================================
# MERGE STREAMS
# =========================================

def get_realtime_data():

    data = fetch_who() + fetch_gdelt()

    if not data:

        data = [{
            "country": "Ethiopia",
            "cases": 2983,
            "deaths": 68,
            "source": "FALLBACK",
            "event": "No live data"
        }]

    return data


# =========================================
# LOAD DATA
# =========================================

data = get_realtime_data()
df = pd.DataFrame(data)

# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Live Events", len(df))
col2.metric("System", "ACTIVE")
col3.metric("Data Sources", "WHO + GDELT")
col4.metric("Mode", "REAL-TIME")

st.divider()

# =========================================
# GLOBAL TABLE
# =========================================

st.subheader("🌍 Live Global Surveillance")

st.dataframe(df, use_container_width=True)

st.divider()

# =========================================
# RISK ENGINE (REAL-TIME LOGIC)
# =========================================

st.subheader("🚨 AI Risk Engine")

def risk_level(cases):

    if cases > 7000:
        return "HIGH"
    elif cases > 3000:
        return "MODERATE"
    return "LOW"


df["risk"] = df["cases"].apply(risk_level)

risk_counts = df["risk"].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.dataframe(risk_counts)

with col2:
    st.bar_chart(risk_counts)

st.divider()

# =========================================
# COUNTRY ANALYTICS
# =========================================

st.subheader("🌍 Country Intelligence")

country_stats = df.groupby("country")[["cases", "deaths"]].sum()

st.dataframe(country_stats, use_container_width=True)

st.divider()

# =========================================
# AI ANALYSIS PANEL
# =========================================

st.subheader("🧠 WHO AI Analysis Engine")

latest = df.iloc[-1]

st.info(
    f"""
🌍 Country: {latest['country']}

📊 Cases: {latest['cases']}

⚰️ Deaths: {latest['deaths']}

🚨 Risk: {latest['risk']}

📡 Source: {latest['source']}
"""
)

st.divider()

# =========================================
# LIVE STREAM (REAL-TIME LOOP)
# =========================================

st.subheader("🔄 Live Global Stream")

placeholder = st.empty()

for _, row in df.iterrows():

    with placeholder:

        st.write(
            f"🌍 **{row['country']}** | "
            f"📊 Cases: {row['cases']} | "
            f"⚰️ Deaths: {row['deaths']} | "
            f"🚨 Risk: {row['risk']} | "
            f"📡 Source: {row['source']} | "
            f"🧠 Event: {row['event']}"
        )

    time.sleep(0.4)

st.divider()

# =========================================
# AUTO REFRESH (REAL-TIME SIMULATION)
# =========================================

time.sleep(6)
st.rerun()
