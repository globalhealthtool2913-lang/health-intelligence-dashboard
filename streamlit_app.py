import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Global Health Intelligence System", layout="wide")

st.title("🌍 Global Health Intelligence System (ML + Prediction)")
st.caption("AI-powered surveillance dashboard — full free intelligence simulation")

# -----------------------------
# SIMULATED GLOBAL DATA
# -----------------------------
np.random.seed(42)

data = pd.DataFrame({
    "country": ["Ethiopia", "Kenya", "Uganda", "Tanzania", "Somalia"],
    "lat": [9.145, -1.286, 1.373, -6.369, 5.152],
    "lon": [40.489, 36.821, 32.290, 34.888, 46.199],
    "cases": np.random.randint(10, 100, 5)
})

# -----------------------------
# ML ANOMALY DETECTION
# -----------------------------
iso = IsolationForest(contamination=0.3, random_state=42)
data["anomaly"] = iso.fit_predict(data[["cases"]])

data["status"] = data["anomaly"].apply(
    lambda x: "🚨 HIGH RISK" if x == -1 else "🟢 NORMAL"
)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Global ML Summary")

col1, col2 = st.columns(2)
col1.metric("🚨 Anomalies", (data["anomaly"] == -1).sum())
col2.metric("🟢 Normal", (data["anomaly"] == 1).sum())

# -----------------------------
# MAP
# -----------------------------
st.subheader("🗺️ Global Risk Map")

data["color"] = data["anomaly"].apply(
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
# DATA TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(data)

# -----------------------------
# PREDICTION ENGINE (ML)
# -----------------------------
st.subheader("🔮 Prediction Engine")

time = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
cases_history = np.array([20, 30, 35, 50, 65, 80])

model = LinearRegression()
model.fit(time, cases_history)

next_case = model.predict([[7]])[0]

st.write(f"📊 Predicted Cases Next Period: **{int(next_case)}**")

if next_case > 70:
    st.error("🚨 High outbreak risk predicted")
elif next_case > 50:
    st.warning("⚠️ Moderate risk predicted")
else:
    st.success("🟢 Low risk predicted")

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend = "INCREASING 📈" if cases_history[-1] > cases_history[0] else "STABLE ➡️"
st.info(f"Global Trend: {trend}")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Data Sources ]
      ↓
[ Feature Engineering ]
      ↓
[ ML Anomaly Detection ]
      ↓
[ Prediction Model ]
      ↓
[ Streamlit Dashboard ]
""")

st.caption("Global Health Intelligence System — ML + Prediction Version")
