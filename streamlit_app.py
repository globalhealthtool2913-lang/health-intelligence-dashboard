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

st.title("🌍 WHO GLOBAL HEALTH INTELLIGENCE DASHBOARD")
st.caption("Production frontend (FastAPI + PostgreSQL backend)")

API_BASE = "http://localhost:8000"

# =========================
# FETCH DATA FROM FASTAPI
# =========================
def get_data():

    try:
        r = requests.get(f"{API_BASE}/signals", timeout=10)

        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()

        # backend returns rows
        df = pd.DataFrame(data)

        if df.empty:
            return df

        df.columns = [
            "id",
            "country",
            "signal",
            "source",
            "timestamp"
        ]

        return df

    except:
        return pd.DataFrame()

df = get_data()

# =========================
# SAFETY CHECK
# =========================
if df.empty:
    st.warning("⚠️ No backend data available (FastAPI or DB not running)")
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

# =========================
# RISK SCORE
# =========================
world["risk"] = (world["signal"] / world["signal"].max()) * 100

# =========================
# METRICS
# =========================
st.subheader("📊 Global Intelligence Overview")

c1, c2 = st.columns(2)

c1.metric("Countries Tracked", len(world))
c2.metric("Average Risk", round(world["risk"].mean(), 2))

# =========================
# MAP VISUALIZATION
# =========================
st.subheader("🗺️ Global Risk Map")

fig = px.choropleth(
    world,
    locations="country",
    locationmode="country names",
    color="risk",
    color_continuous_scale="Reds",
    title="Global Health Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE
# =========================
st.subheader("📋 Intelligence Feed")
st.dataframe(world, use_container_width=True)

# =========================
# TREND LOGIC
# =========================
st.subheader("📈 Global Trend")

if world["risk"].mean() > 60:
    st.error("🚨 Elevated global health activity detected")
elif world["risk"].mean() > 40:
    st.warning("🟡 Moderate activity detected")
else:
    st.success("🟢 Stable global conditions")

# =========================
# SYSTEM INFO
# =========================
st.subheader("🧠 Architecture")

st.code("""
Frontend: Streamlit
Backend: FastAPI
Database: PostgreSQL
Data: GDELT (real-time news signals)
Layer: Aggregation + Risk Scoring
""") 
