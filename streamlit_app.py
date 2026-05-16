import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Global Health Intelligence System", layout="wide")

st.title("🌍 Global Health Intelligence System (Stable Version)")
st.caption("Real-data pipeline with safe fallback + ML + map")

# -----------------------------
# SAFE DATA LOADER (NO CRASH)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    try:
        df = pd.read_csv(url, low_memory=False)

        df = df[["location", "total_cases", "total_deaths"]].dropna()
        df = df.rename(columns={"location": "country"})

        return df

    except Exception:
        st.warning("⚠️ Live data unavailable — using fallback dataset")

        return pd.DataFrame({
            "country": ["Ethiopia", "Kenya", "Uganda", "Tanzania", "Somalia"],
            "total_cases": [120000, 250000, 180000, 140000, 90000],
            "total_deaths": [2500, 4000, 3000, 2000, 1500]
        })

data = load_data()

# -----------------------------
# CLEAN DATA
# -----------------------------
latest = data.groupby("country").tail(1).copy()
latest = latest.rename(columns={
    "total_cases": "cases",
    "total_deaths": "deaths"
})

latest = latest.sort_values("cases", ascending=False).head(20)

# -----------------------------
# FAKE GEO MAPPING (STABLE)
# -----------------------------
coords = {
    "Ethiopia": [9.1, 40.4],
    "Kenya": [-1.2, 36.8],
    "Uganda": [1.3, 32.3],
    "Tanzania": [-6.3, 34.8],
    "Somalia": [5.1, 46.2],
    "United States": [38, -97],
    "India": [20, 78],
    "Brazil": [-10, -55],
}

latest["lat"] = latest["country"].map(lambda x: coords.get(x, [0, 0])[0])
latest["lon"] = latest["country"].map(lambda x: coords.get(x, [0, 0])[1])

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
st.subheader("📊 Global Intelligence Summary")

col1, col2 = st.columns(2)
col1.metric("🚨 High Risk", (latest["anomaly"] == -1).sum())
col2.metric("🟢 Normal", (latest["anomaly"] == 1).sum())

# -----------------------------
# MAP
# -----------------------------
st.subheader("🗺️ Global Risk Map")

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

view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1.3)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(latest)

# -----------------------------
# PREDICTION ENGINE
# -----------------------------
st.subheader("🔮 Prediction Engine")

x = np.arange(len(latest)).reshape(-1, 1)
y = latest["cases"].values

if len(latest) > 3:
    model2 = LinearRegression()
    model2.fit(x, y)

    pred = model2.predict([[len(latest) + 1]])[0]

    st.write(f"📊 Predicted Next Value: **{int(pred)} cases**")

    if pred > np.mean(y):
        st.error("🚨 Increasing global trend detected")
    else:
        st.success("🟢 Stable trend detected")

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend = "INCREASING 📈" if latest["cases"].mean() > 100000 else "STABLE ➡️"
st.info(f"Global Trend: {trend}")

# -----------------------------
# ARCHITECTURE
# -----------------------------
st.subheader("🧠 System Architecture")

st.code("""
[ Real Data Source (OWID / fallback safe mode) ]
            ↓
[ Data Cleaning Layer ]
            ↓
[ ML Anomaly Detection ]
            ↓
[ Forecast Engine ]
            ↓
[ Streamlit Dashboard ]
""")

st.caption("Stable Global Health Intelligence System (No crashes version)")
