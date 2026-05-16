import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(page_title="Global Health Map", layout="wide")

st.title("🌍 Global Health Intelligence Map System")
st.caption("AI-powered surveillance dashboard with geospatial risk mapping")

# -----------------------------
# SIMULATED GLOBAL DATA
# -----------------------------
data = pd.DataFrame({
    "country": ["Ethiopia", "Kenya", "Uganda", "Tanzania", "Somalia"],
    "lat": [9.145, -1.286, 1.373, -6.369, 5.152],
    "lon": [40.489, 36.821, 32.290, 34.888, 46.199],
    "high": np.random.randint(0, 3, 5),
    "moderate": np.random.randint(0, 5, 5),
    "low": np.random.randint(0, 6, 5)
})

# -----------------------------
# RISK SCORE
# -----------------------------
data["score"] = (data["high"] * 4) + (data["moderate"] * 2) + data["low"]

def risk_color(score):
    if score >= 10:
        return [255, 0, 0]      # red
    elif score >= 5:
        return [255, 165, 0]    # orange
    else:
        return [0, 200, 0]      # green

data["color"] = data["score"].apply(risk_color)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Global Risk Summary")

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High Risk", (data["score"] >= 10).sum())
col2.metric("🟠 Moderate Risk", ((data["score"] >= 5) & (data["score"] < 10)).sum())
col3.metric("🟢 Low Risk", (data["score"] < 5).sum())

# -----------------------------
# MAP LAYER
# -----------------------------
st.subheader("🗺️ Global Risk Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_color="color",
    get_radius=500000,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=10,
    longitude=20,
    zoom=1.5
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(data)

# -----------------------------
# TREND SIMULATION
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend = np.random.choice(["Increasing 📈", "Stable ➡️", "Decreasing 📉"])
st.info(f"Global Trend: {trend}")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Global Data Sources ]
        ↓
[ Risk Scoring Engine ]
        ↓
[ Geospatial Mapping Layer ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption("Global Health Intelligence Map System — Free Version")
