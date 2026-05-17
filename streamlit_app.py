import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from sklearn.ensemble import IsolationForest

# ======================================
# CONFIG
# ======================================
st.set_page_config(
    page_title="AI Global Outbreak Intelligence",
    layout="wide"
)

st.title("🌍 AI GLOBAL OUTBREAK PREDICTION SYSTEM")
st.caption("WHO-style intelligence + ML forecasting engine")

# ======================================
# LOAD LIVE DATA (GDELT)
# ======================================
@st.cache_data(ttl=300)
def load_data():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "health OR outbreak OR epidemic OR virus OR disease",
        "mode": "ArtList",
        "maxrecords": 50,
        "format": "json"
    }

    try:
        r = requests.get(url, params=params, timeout=20)

        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()
        articles = data.get("articles", [])

        rows = []

        for a in articles:
            rows.append({
                "country": a.get("sourceCountry", "Unknown"),
                "signal": 1,
                "title": a.get("title", "No Title"),
                "timestamp": a.get("seendate", "2025-01-01")
            })

        return pd.DataFrame(rows)

    except:
        return pd.DataFrame()

# ======================================
# DATA
# ======================================
df = load_data()

# ======================================
# SAFETY FALLBACK
# ======================================
if df.empty:
    st.warning("⚠️ Live data unavailable — using fallback intelligence layer")

    df = pd.DataFrame([
        {"country": "USA", "signal": 5},
        {"country": "India", "signal": 4},
        {"country": "Ethiopia", "signal": 3},
        {"country": "Brazil", "signal": 2}
    ])

# ======================================
# FEATURE ENGINEERING
# ======================================
world = df.groupby("country")["signal"].sum().reset_index()

world["risk_score"] = (
    world["signal"] / world["signal"].max()
) * 100

# ======================================
# AI ANOMALY DETECTION
# ======================================
model = IsolationForest(contamination=0.2, random_state=42)

world["anomaly"] = model.fit_predict(
    world[["signal"]]
)

world["status"] = world["anomaly"].apply(
    lambda x: "🚨 OUTBREAK SIGNAL" if x == -1 else "🟢 NORMAL"
)

# ======================================
# PREDICTION SCORE
# ======================================
world["future_risk"] = (
    world["risk_score"] * 0.7 + world["signal"] * 10
)

# ======================================
# METRICS
# ======================================
st.subheader("📊 Intelligence Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Countries", len(world))
c2.metric("Signals", len(df))
c3.metric("Avg Risk", round(world["risk_score"].mean(), 2))

# ======================================
# MAP
# ======================================
st.subheader("🗺️ Global Risk Map")

fig = px.choropleth(
    world,
    locations="country",
    locationmode="country names",
    color="risk_score",
    color_continuous_scale="Reds",
    title="AI-Powered Global Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# ======================================
# AI OUTBREAK DETECTION
# ======================================
st.subheader("🧠 AI Outbreak Detection")

st.dataframe(world)

# ======================================
# HIGH RISK COUNTRIES
# ======================================
st.subheader("🚨 Predicted High-Risk Zones")

high_risk = world.sort_values(
    "future_risk",
    ascending=False
)

st.dataframe(high_risk)

# ======================================
# TREND ENGINE
# ======================================
st.subheader("📈 Global Trend Prediction")

if world["future_risk"].mean() > 60:
    st.error("🚨 HIGH OUTBREAK RISK DETECTED")
elif world["future_risk"].mean() > 40:
    st.warning("🟡 MODERATE RISK")
else:
    st.success("🟢 STABLE GLOBAL CONDITIONS")

# ======================================
# FUTURE RISK VISUALIZATION
# ======================================
st.subheader("📉 Predicted Risk Distribution")

fig2 = px.bar(
    world,
    x="country",
    y="future_risk",
    color="future_risk",
    title="Forecasted Outbreak Risk by Country"
)

st.plotly_chart(fig2, use_container_width=True)

# ======================================
# ARCHITECTURE
# ======================================
st.subheader("🧠 AI System Architecture")

st.code("""
GDELT Live Data
        ↓
Feature Engineering Layer
        ↓
Isolation Forest (Anomaly Detection)
        ↓
Risk Scoring Engine
        ↓
Prediction Layer
        ↓
Streamlit AI Dashboard
""")

st.caption("AI-powered global outbreak early warning system")
