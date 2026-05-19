 import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import feedparser
from sklearn.ensemble import IsolationForest
from datetime import datetime
import queue

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="WHO Distributed AI System",
    layout="wide"
)

st.title("🌍 WHO Distributed AI Intelligence System")
st.caption("Microservices + AI Agents + Event Streaming (Prototype)")

# =========================
# EVENT BUS (Kafka-like simulation)
# =========================
event_bus = queue.Queue()

def publish_event(event):
    event_bus.put(event)

def consume_events():
    events = []
    while not event_bus.empty():
        events.append(event_bus.get())
    return events

# =========================
# LIVE HEALTH DATA
# =========================
@st.cache_data(ttl=120)
def load_health_data():

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
        df = pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        })
        return df, False


df, live = load_health_data()

if live:
    st.success("🟢 LIVE DATA ACTIVE")
else:
    st.warning("🔴 OFFLINE MODE")

# =========================
# 🧠 AI AGENTS (MICROSERVICES STYLE)
# =========================

def risk_agent(df):

    df["risk_score"] = (
        df["Cases"] * 0.4 +
        df["Deaths"] * 0.4 +
        (100 - df["Policy"]) * 0.2
    )

    return df


def anomaly_agent(df):

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(df[["risk_score"]])

    df["anomaly"] = df["anomaly"].apply(
        lambda x: "ALERT" if x == -1 else "OK"
    )

    return df


def forecast_agent(df):

    df["forecast"] = df["risk_score"].rolling(2).mean().fillna(df["risk_score"])

    return df


def orchestrator(df):

    df = risk_agent(df)
    df = anomaly_agent(df)
    df = forecast_agent(df)

    return df

# =========================
# RUN AI PIPELINE
# =========================
df = orchestrator(df)

# =========================
# SIMULATE BACKEND EVENTS
# =========================
for _, row in df.iterrows():

    if row["anomaly"] == "ALERT":

        publish_event({
            "type": "OUTBREAK_ALERT",
            "country": row["Country"],
            "risk": float(row["risk_score"]),
            "time": str(datetime.utcnow())
        })

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🌍 Filters")

countries = st.sidebar.multiselect(
    "Countries",
    df["Country"].tolist(),
    default=df["Country"].tolist()
)

min_risk = st.sidebar.slider(
    "Minimum Risk",
    0,
    int(df["risk_score"].max()),
    0
)

filtered = df[
    (df["Country"].isin(countries)) &
    (df["risk_score"] >= min_risk)
]

# =========================
# METRICS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Countries", len(filtered))
c2.metric("Avg Risk", round(filtered["risk_score"].mean(), 2))
c3.metric("Max Risk", round(filtered["risk_score"].max(), 2))
c4.metric("Alerts", int((filtered["anomaly"] == "ALERT").sum()))

# =========================
# ALERT SYSTEM
# =========================
st.subheader("🚨 Live Outbreak Alerts")

alerts = filtered[filtered["anomaly"] == "ALERT"]

if alerts.empty:
    st.success("No active outbreaks detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → HIGH RISK ({row['risk_score']:.2f})")

# =========================
# WHO RSS FEED
# =========================
st.subheader("📰 WHO Intelligence Feed")

try:
    feed = feedparser.parse(
        "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
    )

    for entry in feed.entries[:5]:
        st.markdown(f"• {entry.title}")

except:
    st.warning("WHO feed unavailable")

# =========================
# EVENT STREAM (KAFKA-LIKE)
# =========================
st.subheader("📡 Event Stream (Kafka Simulation)")

events = consume_events()

if events:

    for e in events:

        st.write(e)

else:
    st.info("No active outbreak events")

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    filtered,
    locations="Country",
    locationmode="country names",
    color="risk_score",
    hover_name="Country"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# FORECASTING
# =========================
st.subheader("📈 Forecast Engine")

st.bar_chart(filtered.set_index("Country")["forecast"])

# =========================
# AI SUMMARY AGENT
# =========================
st.subheader("🧠 AI Situation Report")

top = filtered.sort_values("risk_score", ascending=False).head(3)

summary = " ".join([
    f"{r['Country']} shows elevated epidemic risk."
    for _, r in top.iterrows()
])

st.info(summary)

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Intelligence Dataset")

st.dataframe(filtered)

# =========================
# EXPORT
# =========================
csv = filtered.to_csv(index=False).encode()

st.download_button(
    "⬇ Export Intelligence Report",
    csv,
    "who_distributed_system.csv",
    "text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("WHO Distributed AI System | Microservices Prototype")
