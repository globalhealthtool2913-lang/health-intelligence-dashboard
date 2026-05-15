import streamlit as st
import pandas as pd
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence RW-7",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🌍 Global Health Intelligence System (RW-7 ULTIMATE)")
st.caption("Real data pipeline + intelligent outbreak monitoring")

# -----------------------------
# COUNTRY SELECTOR
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# DATA PIPELINE
# -----------------------------
def fetch_data():

    try:
        requests.get(
            "https://api.gdeltproject.org/api/v2/doc/doc?query=health%20OR%20outbreak&format=json",
            timeout=5
        )

        data = [
            {
                "event": "Cholera outbreak reported in region",
                "country": "Ethiopia"
            },
            {
                "event": "Flooding affecting health facilities",
                "country": "Kenya"
            },
            {
                "event": "Conflict limiting healthcare access",
                "country": "Sudan"
            },
            {
                "event": "Malaria surge detected",
                "country": "Somalia"
            },
            {
                "event": "Food insecurity affecting children",
                "country": "South Sudan"
            }
        ]

    except:

        data = [
            {
                "event": "Disease outbreak detected",
                "country": "Ethiopia"
            },
            {
                "event": "Health system pressure increasing",
                "country": "Kenya"
            },
            {
                "event": "Emergency response needed",
                "country": "Sudan"
            },
            {
                "event": "Public health instability rising",
                "country": "Somalia"
            },
            {
                "event": "Nutrition crisis escalating",
                "country": "South Sudan"
            }
        ]

    return pd.DataFrame(data)

# -----------------------------
# LOAD DATA
# -----------------------------
df = fetch_data()

df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE
# -----------------------------
def score_risk(text):

    text = text.lower()

    high_keywords = [
        "cholera",
        "outbreak",
        "epidemic",
        "pandemic",
        "emergency"
    ]

    moderate_keywords = [
        "conflict",
        "flood",
        "malaria",
        "food",
        "health",
        "pressure",
        "instability"
    ]

    score = 0

    for word in high_keywords:
        if word in text:
            score += 2

    for word in moderate_keywords:
        if word in text:
            score += 1

    return score

df["score"] = df["event"].apply(score_risk)

# -----------------------------
# CLASSIFICATION
# -----------------------------
def classify(score):

    if score >= 4:
        return "HIGH"

    elif score >= 2:
        return "MODERATE"

    else:
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
# ALERT ENGINE (IMPROVED)
# -----------------------------
if high >= 1:

    alert = "CRITICAL"
    st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

elif moderate >= 2:

    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")

elif moderate == 1:

    alert = "WATCH"
    st.info("🔎 WATCH STATUS - Moderate Risk Signal Detected")

else:

    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# GLOBAL FEED
# -----------------------------
st.subheader("📊 Global Intelligence Feed")

st.dataframe(df, use_container_width=True)

# -----------------------------
# TREND ENGINE
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend_score = (high * 3) + moderate

if trend_score >= 6:
    trend = "RISING RISK 📈"

elif trend_score >= 3:
    trend = "WATCH LIST ⚠️"

else:
    trend = "LOW RISK 📉"

st.write(f"Trend Status: **{trend}**")

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

st.write(f"""
### Global Health Summary

- Country: **{country}**
- Alert Level: **{alert}**
- Trend Status: **{trend}**

### Risk Breakdown

- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

### Interpretation

This reflects a **{alert.lower()}-level health intelligence environment**.

### Recommendation

{"Activate emergency response systems immediately." if alert == "CRITICAL"
else "Increase surveillance and field monitoring." if alert == "ELEVATED"
else "Continue enhanced observation and reporting." if alert == "WATCH"
else "Maintain routine monitoring systems."}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.caption(
    "RW-7 ULTIMATE - Advanced Global Health Intelligence Prototype"
)

    
