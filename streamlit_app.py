import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import pydeck as pdk

st.set_page_config(page_title="Global Health ML Dashboard", layout="wide")

st.title("🌍 Global Health Intelligence System (ML Version)")
st.caption("AI-powered outbreak detection + anomaly monitoring")

# -----------------------------
# SIMULATED GLOBAL DATA
# -----------------------------
np.random.seed(42)

data = pd.DataFrame({
    "country": ["Ethiopia", "Kenya", "Uganda", "Tanzania", "Somalia"],
    "lat": [9.145, -1.286, 1.373, -6.369, 5.152],
    "lon": [40.489, 36.821, 32.290, 34.888, 46.199],
    "cases": np.random.randint(5, 100, 5)
})

# -----------------------------
# ML MODEL (ANOMALY DETECTION)
# -----------------------------
model = IsolationForest(contamination=0.3, random_state=42)

data["anomaly_score"] = model.fit_predict(data[["cases"]])

# Convert ML output
def risk_label(x):
    if x == -1:
        return "🚨 ANOMALY (HIGH RISK)"
    else:
        return "🟢 NORMAL"

data["status"] = data["anomaly_score"].apply(risk_label)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 ML Risk Summary")

anomalies = (data["anomaly_score"] == -1).sum()
normal = (data["anomaly_score"] == 1).sum()

col1, col2 = st.columns(2)
col1.metric("🚨 Anomalies Detected", anomalies)
col2.metric("🟢 Normal Regions", normal)

# -----------------------------
# MAP VISUALIZATION
# -----------------------------
st.subheader("🗺️ ML Risk Map")

data["color"] = data["anomaly_score"].apply(
    lambda x: [255, 0, 0] if x == -1 else [0, 200, 0]
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_color="color",
    get_radius=600000,
    pickable=True
)

view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1.5)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed (ML Output)")
st.dataframe(data)

# -----------------------------
# SIMPLE FORECAST LOGIC
# -----------------------------
st.subheader("📈 Trend Forecast (Simple ML Signal)")

trend_signal = "INCREASING 📈" if data["cases"].mean() > 50 else "STABLE ➡️"

st.info(f"Forecast: {trend_signal}")

# -----------------------------
# ALERT ENGINE
# -----------------------------
st.subheader("🚨 Alert Engine")

if anomalies > 0:
    st.error("High-risk anomaly detected in global dataset!")
else:
    st.success("System stable — no anomalies detected")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Data Sources ]
      ↓
[ Feature Engineering ]
      ↓
[ ML Model: Isolation Forest ]
      ↓
[ Anomaly Detection Engine ]
      ↓
[ Streamlit Dashboard ]
""")

st.caption("ML-powered Global Health Intelligence System (Free Version)")
