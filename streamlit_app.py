
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Global Health Intelligence", layout="wide")

st.title("🌍 Global Health Intelligence System (Free Version)")
st.caption("AI-powered surveillance dashboard — offline intelligence simulation")

# -----------------------------
# SIMULATED DATA (MULTI-COUNTRY)
# -----------------------------
countries = ["Ethiopia", "Kenya", "Uganda", "Tanzania", "Somalia"]

data = pd.DataFrame({
    "country": countries,
    "high": np.random.randint(0, 3, len(countries)),
    "moderate": np.random.randint(0, 5, len(countries)),
    "low": np.random.randint(0, 6, len(countries))
})

# -----------------------------
# RISK SCORING MODEL
# -----------------------------
data["score"] = (data["high"] * 4) + (data["moderate"] * 2) + data["low"]

def risk_level(score):
    if score >= 10:
        return "HIGH"
    elif score >= 5:
        return "MODERATE"
    else:
        return "LOW"

data["risk"] = data["score"].apply(risk_level)

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
country = st.sidebar.selectbox("Select Country", data["country"])
filtered = data[data["country"] == country]

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Country Risk Overview")

high = (data["risk"] == "HIGH").sum()
moderate = (data["risk"] == "MODERATE").sum()
low = (data["risk"] == "LOW").sum()

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# SELECTED COUNTRY DETAILS
# -----------------------------
st.subheader(f"🌍 {country} Intelligence Profile")

st.dataframe(filtered, use_container_width=True)

# -----------------------------
# TREND SIMULATION
# -----------------------------
st.subheader("📈 Trend Intelligence (Simulated)")

trend = np.random.choice(["Increasing 📈", "Stable ➡️", "Decreasing 📉"])

st.info(f"Current Trend: {trend}")

# -----------------------------
# SIMPLE BAR CHART
# -----------------------------
st.subheader("📊 Risk Score Comparison")

chart_data = data.set_index("country")[["high", "moderate", "low"]]
st.bar_chart(chart_data)

# -----------------------------
# GLOBAL SUMMARY
# -----------------------------
st.subheader("🌍 Global Intelligence Summary")

st.write(data)

# -----------------------------
# AUTO REFRESH SIMULATION
# -----------------------------
st.caption("Refreshing simulation every 10 seconds...")

time.sleep(1)
st.rerun()

