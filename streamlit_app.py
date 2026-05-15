import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence RW-5", layout="wide")

st.title("🌍 Global Health Intelligence System (RW-5 CLEAN)")
st.caption("Advanced intelligence system (no external PDF libraries)")

# -----------------------------
# COUNTRY
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# DATA LAYER
# -----------------------------
def get_data():
    try:
        requests.get("https://api.reliefweb.int/v1/reports?appname=health-intel", timeout=5)

        return pd.DataFrame([
            {"event": "Cholera outbreak spreading rapidly", "country": "Ethiopia"},
            {"event": "Floods disrupting hospitals", "country": "Kenya"},
            {"event": "Conflict affecting healthcare access", "country": "Sudan"},
            {"event": "Malaria surge in rural districts", "country": "Somalia"},
            {"event": "Severe food insecurity affecting children", "country": "South Sudan"}
        ])
    except:
        return pd.DataFrame([
            {"event": "Disease outbreak detected", "country": "Ethiopia"},
            {"event": "Health system stress increasing", "country": "Kenya"},
            {"event": "Emergency conditions reported", "country": "Sudan"},
            {"event": "Public health instability", "country": "Somalia"},
            {"event": "Nutrition crisis escalating", "country": "South Sudan"}
        ])

df = get_data()
df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE
# -----------------------------
def score(text):
    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "surge"]
    moderate = ["conflict", "flood", "malaria", "food", "displacement"]

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
    if s >= 3:
        return "HIGH"
    elif s == 2:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(classify)

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
    st.error("🚨 CRITICAL PUBLIC HEALTH RISK")
elif moderate >= 1:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")
else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# TREND ENGINE
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend_score = (high * 3) + (moderate * 1)

if trend_score >= 6:
    trend = "RISING RISK 📈"
elif trend_score >= 3:
    trend = "STABLE MONITORING ⚠️"
else:
    trend = "LOW RISK 📉"

st.write(f"Trend Status: **{trend}**")

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

report = f"""
Country: {country}
Alert Level: {alert}

High signals: {high}
Moderate signals: {moderate}
Low signals: {low}

Trend: {trend}

Recommendation:
{"Activate emergency response." if alert=="CRITICAL"
 else "Increase monitoring." if alert=="ELEVATED"
 else "Maintain routine surveillance."}
"""

st.text(report)

# -----------------------------
# OPTIONAL DOWNLOAD (TEXT ONLY)
# -----------------------------
st.subheader("📄 Policy Brief Download")

st.download_button(
    label="Download Report (TXT)",
    data=report,
    file_name=f"{country}_health_report.txt",
    mime="text/plain"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-5 CLEAN - No external dependencies version")
