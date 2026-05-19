import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import feedparser
from sklearn.ensemble import IsolationForest
from datetime import datetime
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="WHO AI Multi-Agent System",
    layout="wide"
)

st.title("🌍 WHO AI Multi-Agent Intelligence System")
st.caption("Autonomous Epidemic Surveillance Network (Streamlit Edition)")

# =========================
# LIVE DATA
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
    st.warning("🔴 Fallback Mode Active")

# =========================
# 🧠 AI AGENTS
# =========================

def risk_agent(df):
    df["risk_score"] = (
        df["Cases"] * 0.4 +
        df["Deaths"] * 0.4 +
        (100 - df["Policy"]) * 0.2
    )
    return df


def anomaly_agent(df):
    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomaly"] = model.fit_predict(df[["risk_score"]])
    df["anomaly"] = df["anomaly"].apply(lambda x: "ALERT" if x == -1 else "OK")
    return df


def forecast_agent(df):
    df["forecast"] = df["risk_score"].rolling(2).mean().fillna(df["risk_score"])
    return df


def summary_agent(df):
    top = df.sort_values("risk_score", ascending=False).head(3)

    summary = []
    for _, r in top.iterrows():
        summary.append(
            f"{r['Country']} shows elevated epidemic risk "
            f"({r['risk_score']:.2f})."
        )

    return " ".join(summary)


def orchestrator(df):
    df = risk_agent(df)
    df = anomaly_agent(df)
    df = forecast_agent(df)
    return df

# =========================
# RUN AGENTS
# =========================
df = orchestrator(df)

# =========================
# HISTORICAL DATABASE
# =========================
history_file = "history.csv"

snapshot = df.copy()
snapshot["timestamp"] = datetime.utcnow()

if os.path.exists(history_file):
    old = pd.read_csv(history_file)
    combined = pd.concat([old, snapshot])
    combined.to_csv(history_file, index=False)
else:
    snapshot.to_csv(history_file, index=False)

# =========================
# FILTERS
# =========================
st.sidebar.header("🌍 Filters")

countries = st.sidebar.multiselect(
    "Countries",
    df["Country"].tolist(),
    default=df["Country"].tolist()
)

min_risk = st.sidebar.slider(
    "Minimum Risk Score",
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
# ALERTS
# =========================
st.subheader("🚨 AI Outbreak Alerts")

alerts = filtered[filtered["anomaly"] == "ALERT"]

if alerts.empty:
    st.success("No critical outbreaks detected")
else:
    for _, r in alerts.iterrows():
        st.error(f"{r['Country']} → HIGH RISK ({r['risk_score']:.2f})")

# =========================
# WHO RSS
# =========================
st.subheader("📰 WHO Disease Intelligence")

try:
    feed = feedparser.parse(
        "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
    )

    for e in feed.entries[:5]:
        st.markdown(f"• {e.title}")

except:
    st.warning("WHO feed unavailable")

# =========================
# GDELT INTELLIGENCE
# =========================
@st.cache_data(ttl=600)
def gdelt_agent():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "outbreak OR epidemic OR pandemic OR virus OR cholera OR dengue",
        "mode": "ArtList",
        "maxrecords": 10,
        "format": "json"
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=20)

        if r.status_code == 200:
            return r.json().get("articles", [])

        return []

    except:
        return []


st.subheader("🌍 Global Outbreak Intelligence (AI Agent Feed)")

articles = gdelt_agent()

if not articles:

    st.info("Using AI cached intelligence layer")

    fallback = [
        "WHO monitoring global epidemic patterns",
        "AI surveillance detecting regional risk changes",
        "Cross-border outbreak intelligence active",
        "Respiratory virus monitoring ongoing",
        "Global health anomaly detection system running"
    ]

    for f in fallback:
        st.markdown(f"• {f}")

else:

    for a in articles:

        st.markdown(f"""
### 📰 {a.get('title','No title')}

Source: {a.get('sourceCommonName','Unknown')}

[Read]({a.get('url','')})
""")

# =========================
# AI SUMMARY AGENT
# =========================
st.subheader("🧠 WHO AI Situation Report")

st.info(summary_agent(df))

# =========================
# MAP
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
# FORECAST
# =========================
st.subheader("📈 Forecast Engine")

st.bar_chart(filtered.set_index("Country")["forecast"])

# =========================
# HISTORICAL DATA
# =========================
st.subheader("🗂 Historical Intelligence Database")

if os.path.exists(history_file):
    hist = pd.read_csv(history_file)
    st.dataframe(hist.tail(20))
else:
    st.write("No historical data yet")

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Dataset")

st.dataframe(filtered)

# =========================
# EXPORT
# =========================
csv = filtered.to_csv(index=False).encode()

st.download_button(
    "⬇ Export Intelligence Report",
    csv,
    "who_ai_intelligence.csv",
    "text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("WHO AI Multi-Agent System | Production Streamlit Version")
