import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="RW-10 Global Health Intelligence", layout="wide")

st.title("🌍 Global Health Intelligence Platform (RW-10)")
st.caption("Operational outbreak intelligence system with trends, sources, and exports")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

risk_filter = st.sidebar.multiselect(
    "Filter Risk Level",
    ["HIGH", "MODERATE", "LOW"],
    default=["HIGH", "MODERATE", "LOW"]
)

source_filter = st.sidebar.multiselect(
    "Filter Source",
    ["WHO", "Africa CDC", "UNICEF", "ReliefWeb"],
    default=["WHO", "Africa CDC", "UNICEF", "ReliefWeb"]
)

# -----------------------------
# DATA (SIMULATED REAL-WORLD STRUCTURE)
# -----------------------------
data = [
    {
        "event": "Cholera outbreak reported",
        "country": "Ethiopia",
        "source": "WHO",
        "date": "2026-05-15"
    },
    {
        "event": "Flooding affecting hospitals",
        "country": "Kenya",
        "source": "ReliefWeb",
        "date": "2026-05-14"
    },
    {
        "event": "Conflict limiting healthcare access",
        "country": "Sudan",
        "source": "UNICEF",
        "date": "2026-05-13"
    },
    {
        "event": "Malaria surge detected",
        "country": "Somalia",
        "source": "Africa CDC",
        "date": "2026-05-12"
    },
    {
        "event": "Food insecurity crisis escalating",
        "country": "South Sudan",
        "source": "WHO",
        "date": "2026-05-11"
    }
]

df = pd.DataFrame(data)

# -----------------------------
# FILTER DATA
# -----------------------------
df = df[df["country"] == country]
df = df[df["source"].isin(source_filter)]

# -----------------------------
# RISK ENGINE
# -----------------------------
def score(text):
    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "pandemic", "emergency"]
    moderate = ["flood", "conflict", "malaria", "food", "health"]

    s = 0

    for w in high:
        if w in text:
            s += 2

    for w in moderate:
        if w in text:
            s += 1

    return s

df["score"] = df["event"].apply(score)

def classify(s):
    if s >= 4:
        return "HIGH"
    elif s >= 2:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(classify)

df = df[df["risk"].isin(risk_filter)]

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT ENGINE
# -----------------------------
if high >= 1:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

elif moderate >= 2:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")

elif moderate == 1:
    alert = "WATCH"
    st.info("🔎 WATCH STATUS")

else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# TREND ANALYTICS
# -----------------------------
st.subheader("📈 Trend Analysis")

trend_score = (high * 3) + moderate

if trend_score >= 6:
    trend = "RISING RISK 📈"
elif trend_score >= 3:
    trend = "WATCH LIST ⚠️"
else:
    trend = "LOW RISK 📉"

st.write(f"Trend Status: **{trend}**")

# chart
fig, ax = plt.subplots()
ax.plot([high, moderate, low])
ax.set_title("Risk Trend Snapshot")
st.pyplot(fig)

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

report = f"""
Country: {country}
Date: {datetime.now().strftime('%Y-%m-%d')}

Alert Level: {alert}
Trend: {trend}

High signals: {high}
Moderate signals: {moderate}
Low signals: {low}

Recommendation:
{"Activate emergency response immediately." if alert=="CRITICAL"
else "Increase surveillance and monitoring." if alert=="ELEVATED"
else "Maintain routine monitoring."}
"""

st.text(report)

# -----------------------------
# EXPORT
# -----------------------------
st.download_button(
    "⬇️ Download Report",
    report,
    file_name=f"{country}_RW10_report.txt"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-10 - Operational Global Health Intelligence Platform")
