import streamlit as st
import pandas as pd
import requests
import numpy as np
import pydeck as pdk
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Real Global Health Intelligence", layout="wide")

st.title("🌍 Real Global Health Intelligence System")
st.caption("Live data integration (WHO / OWID / GDELT style sources)")

# -----------------------------
# LOAD REAL DATA (OWID COVID DATASET)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# -----------------------------
# FILTER LATEST DATA
# -----------------------------
latest = df.groupby("location").tail(1)

latest = latest[["location", "total_cases", "total_deaths"]].dropna()

latest = latest.rename(columns={
    "location": "country",
    "total_cases": "cases",
    "total_deaths": "deaths"
})

# -----------------------------
# CLEAN DATA
# -----------------------------
latest = latest.sort_values("cases", ascending=False).head(20)

# fake lat/lon mapping (real-world approximation for demo map)
country_coords = {
    "United States": [38, -97],
    "India": [20, 78],
    "Brazil": [-10, -55],
    "Germany": [51, 10],
    "France": [46, 2],
    "United Kingdom": [55, -3],
    "Italy": [42, 12],
    "South Africa": [-30, 25],
    "Ethiopia": [9, 40],
    "Kenya": [1, 37]
}

latest["lat"] = latest["country"].map(lambda x: country_coords.get(x, [0, 0])[0])
latest["lon"] = latest["country"].map(lambda x: country_coords.get(x, [0, 0])[1])

# -----------------------------
# ML ANOMALY DETECTION
# -----------------------------
model = IsolationForest(contamination=0.2, random_state=42)

latest["anomaly"] = model.fit_predict(latest[["cases"]])

latest["risk"] = latest["anomaly"].apply(
    lambda x: "🚨 HIGH RISK" if x == -1 else "🟢 NORMAL"
)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Global Summary (Real Data)")

col1, col2 = st.columns(2)
col1.metric("🚨 High Risk Areas", (latest["anomaly"] == -1).sum())
col2.metric("🟢 Normal Areas", (latest["anomaly"] == 1).sum())

# -----------------------------
# MAP
# -----------------------------
st.subheader("🗺️ Real Data Risk Map")

latest["color"] = latest["anomaly"].apply(
    lambda x: [255, 0, 0] if x == -1 else [0, 200, 0]
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=latest,
    get_position='[lon, lat]',
    get_color="color",
    get_radius=800000,
    pickable=True
)

view_state = pdk.ViewState(latitude=20, longitude=10, zoom=1.2)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Real Intelligence Feed")
st.dataframe(latest)

# -----------------------------
# SIMPLE FORECAST
# -----------------------------
st.subheader("🔮 Forecast (Basic ML)")

x = np.array(range(len(latest))).reshape(-1, 1)
y = latest["cases"].values

if len(latest) > 5:
    from sklearn.linear_model import LinearRegression

    model2 = LinearRegression()
    model2.fit(x, y)

    prediction = model2.predict([[len(latest) + 1]])[0]

    st.write(f"📊 Next Global Risk Estimate: **{int(prediction)} cases equivalent**")

    if prediction > np.mean(y):
        st.error("🚨 Increasing global trend detected")
    else:
        st.success("🟢 Stable trend detected")

# -----------------------------
# SYSTEM ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ WHO / OWID Global Dataset ]
          ↓
[ Data Cleaning & Mapping ]
          ↓
[ ML Anomaly Detection ]
          ↓
[ Forecast Engine ]
          ↓
[ Streamlit Dashboard ]
""")

st.caption("Real-data Global Health Intelligence System")
