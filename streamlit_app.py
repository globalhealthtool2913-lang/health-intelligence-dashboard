import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="WHO Global Intelligence",
    layout="wide"
)

st.title("🌍 WHO GLOBAL HEALTH INTELLIGENCE")
st.caption("Stable production dashboard (Streamlit Cloud ready)")

# =========================
# BACKEND API (CHANGE IF DEPLOYED)
# =========================
API_URL = "https://your-backend-url.com/signals"

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=60)
def load_data():

    try:
        r = requests.get(API_URL, timeout=10)

        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()

        df = pd.DataFrame(data)

        if df.empty:
            return df

        df.columns = ["id", "country", "signal", "source", "timestamp"]

        return df

    except:
        return pd.DataFrame()

df = load_data()

# =========================
# SAFETY CHECK
# =========================
if df.empty:
    st.warning("⚠️ No data available (backend not connected or API failed)")
    st.stop()

# =========================
# CLEANING
# =========================
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# =========================
# AGGREGATION
# =========================
world = df.groupby("country")["signal"].sum().reset_index()

world["risk"] = (world["signal"] / world["signal"].max()) * 100

# =========================
# METRICS
# =========================
st.subheader("📊 Global Intelligence Overview")

c1, c2 = st.columns(2)

c1.metric("Countries", len(world))
c2.metric("Average Risk", round(world["risk"].mean(), 2))

# =========================
# MAP
# =========================
st.subheader("🗺️ Global Risk Map")

fig = px.choropleth(
    world,
    locations="country",
    locationmode="country names",
    color="risk",
    color_continuous_scale="Reds",
    title="Global Health Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE
# =========================
st.subheader("📋 Intelligence Feed")
st.dataframe(world, use_container_width=True)

# =========================
# TREND
# =========================
st.subheader("📈 Global Trend")

if world["risk"].mean() > 60:
    st.error("🚨 High global activity detected")
elif world["risk"].mean() > 40:
    st.warning("🟡 Moderate activity")
else:
    st.success("🟢 Stable conditions")

# =========================
# ARCHITECTURE
# =========================
st.subheader("🧠 System Architecture")

st.code("""
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
PostgreSQL Database
        ↓
GDELT Live Data
        ↓
Aggregation + Risk Engine
""")
