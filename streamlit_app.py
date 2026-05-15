import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence RW-9",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🌍 RW-9 Operations Center")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Regional Monitoring",
        "Trend Analytics",
        "AI Situation Report"
    ]
)

country = st.sidebar.selectbox(
    "Select Country",
    [
        "Ethiopia",
        "Kenya",
        "Sudan",
        "Somalia",
        "South Sudan"
    ]
)

# -----------------------------
# DATA
# -----------------------------
data = [
    {
        "event": "Cholera outbreak reported",
        "country": "Ethiopia",
        "lat": 9.03,
        "lon": 38.74
    },
    {
        "event": "Flooding affecting hospitals",
        "country": "Kenya",
        "lat": -1.28,
        "lon": 36.82
    },
    {
        "event": "Conflict limiting healthcare",
        "country": "Sudan",
        "lat": 15.50,
        "lon": 32.56
    },
    {
        "event": "Malaria surge detected",
        "country": "Somalia",
        "lat": 2.04,
        "lon": 45.34
    },
    {
        "event": "Food insecurity crisis",
        "country": "South Sudan",
        "lat": 4.85,
        "lon": 31.60
    }
]

df = pd.DataFrame(data)

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
        "crisis"
    ]

    moderate_keywords = [
        "flood",
        "conflict",
        "malaria",
        "food",
        "health"
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

high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if page == "Dashboard":

    st.title("🌍 Global Health Intelligence Operations Center")
    st.caption("RW-9 Intelligence & Surveillance Dashboard")

    st.info(f"Monitoring: {country}")

    col1, col2, col3 = st.columns(3)

    col1.metric("🔴 High", high)
    col2.metric("🟠 Moderate", moderate)
    col3.metric("🟢 Low", low)

    st.divider()

    if high >= 1:

        alert = "CRITICAL"
        st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

    elif moderate >= 2:

        alert = "ELEVATED"
        st.warning("⚠️ ELEVATED HEALTH RISK")

    elif moderate == 1:

        alert = "WATCH"
        st.info("🔎 WATCH STATUS - Moderate Risk Signal")

    else:

        alert = "STABLE"
        st.success("🟢 STABLE CONDITIONS")

    st.subheader("📊 Intelligence Feed")
    st.dataframe(df, use_container_width=True)

# -----------------------------
# MAP PAGE
# -----------------------------
elif page == "Regional Monitoring":

    st.title("🗺️ Regional Monitoring")

    st.write("Live regional health surveillance mapping")

    map_df = df[["lat", "lon"]]

    st.map(map_df)

    st.dataframe(df)

# -----------------------------
# ANALYTICS PAGE
# -----------------------------
elif page == "Trend Analytics":

    st.title("📈 Trend Analytics")

    fig, ax = plt.subplots()

    categories = ["High", "Moderate", "Low"]
    values = [high, moderate, low]

    ax.bar(categories, values)

    ax.set_ylabel("Signal Count")
    ax.set_title("Health Risk Distribution")

    st.pyplot(fig)

    trend_score = (high * 3) + moderate

    if trend_score >= 6:
        trend = "RISING RISK 📈"

    elif trend_score >= 3:
        trend = "WATCH LIST ⚠️"

    else:
        trend = "LOW RISK 📉"

    st.subheader("Trend Status")
    st.write(f"**{trend}**")

# -----------------------------
# AI REPORT PAGE
# -----------------------------
elif page == "AI Situation Report":

    st.title("🧠 AI Situation Report")

    if high >= 1:
        alert = "CRITICAL"

    elif moderate >= 2:
        alert = "ELEVATED"

    elif moderate == 1:
        alert = "WATCH"

    else:
        alert = "STABLE"

    st.write(f"""
    ### Global Health Intelligence Summary

    - Country Focus: **{country}**
    - Alert Level: **{alert}**

    ### Risk Analysis

    - High-risk signals: {high}
    - Moderate-risk signals: {moderate}
    - Low-risk signals: {low}

    ### Interpretation

    Current intelligence reflects a
    **{alert.lower()}-level public health environment**.

    ### Recommendation

    {"Activate emergency coordination immediately." if alert == "CRITICAL"
    else "Increase field surveillance and monitoring." if alert == "ELEVATED"
    else "Maintain enhanced observation and reporting." if alert == "WATCH"
    else "Continue routine monitoring systems."}
    """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.caption(
    "RW-9 Intelligence Operations Center"
)
