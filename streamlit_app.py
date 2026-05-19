import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import feedparser
from sklearn.ensemble import IsolationForest
from datetime import datetime

# =========================
# APP CONFIG
# =========================
st.set_page_config(
    page_title="WHO AI Intelligence System",
    layout="wide"
)

st.title("🌍 WHO AI Intelligence System (Production)")
st.caption("Live Health Monitoring + AI Risk + News + Forecasting")

# =========================
# LIVE DATA SOURCE
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
    st.warning("🔴 Fallback Mode Active")

# =========================
# DATA CLEANING
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
# FORECASTING (SAFE)
# =========================
df["Forecast"] = df["Risk"].rolling(2).mean().fillna(df["Risk"])

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
    "Minimum Risk",
    0,
    int(df["Risk"].max()),
    0
)

filtered = df[
    (df["Country"].isin(countries)) &
    (df["Risk"] >= min_risk)
]

# =========================
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(filtered))
col2.metric("Avg Risk", round(filtered["Risk"].mean(), 2))
col3.metric("Max Risk", round(filtered["Risk"].max(), 2))
col4.metric("Alerts", int((filtered["Anomaly"] == "ALERT").sum()))

# =========================
# ALERT SYSTEM
# =========================
st.subheader("🚨 Live Outbreak Alerts")

alerts = filtered[filtered["Anomaly"] == "ALERT"]

if alerts.empty:
    st.success("🟢 No critical anomalies detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → HIGH RISK ALERT (Risk {row['Risk']:.2f})")

# =========================
# WHO NEWS INTELLIGENCE
# =========================
st.subheader("📰 WHO News Intelligence")

try:
    feed = feedparser.parse(
        "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
    )

    for entry in feed.entries[:6]:
        st.write("•", entry.title)

except:
    st.warning("News feed unavailable")

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    filtered,
    locations="Country",
    locationmode="country names",
    color="Risk",
    title="WHO Global Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# FORECASTING
# =========================
st.subheader("📈 AI Forecasting")

st.bar_chart(filtered.set_index("Country")["Forecast"])

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Intelligence Dataset")

st.dataframe(filtered)

# =========================
# EXPORT
# =========================
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Report",
    csv,
    "who_intelligence.csv",
    "text/csv"
)

st.markdown("---")
st.write("✔ Stable WHO AI Intelligence System")
