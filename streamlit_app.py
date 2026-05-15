import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v3",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v3")
st.markdown("Advanced AI-assisted monitoring for global health risks")

# -----------------------------
# COUNTRY FILTER
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring health risks for: {country}")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"title": "Conflict impacts health services", "category": "Conflict"},
    {"title": "Disease outbreak monitoring", "category": "Disease"},
    {"title": "Child health progress", "category": "Child Health"},
    {"title": "Health system strengthening", "category": "Routine"}
]

df = pd.DataFrame(data)

# -----------------------------
# RISK MODEL (IMPROVED)
# -----------------------------
def score_risk(text):
    text = text.lower()
    score = 0

    if "conflict" in text:
        score += 35
    if "outbreak" in text:
        score += 35
    if "child" in text:
        score += 20
    if "health" in text:
        score += 10

    return score

df["score"] = df["title"].apply(score_risk)

def risk_level(score):
    if score >= 60:
        return "HIGH"
    elif score >= 35:
        return "MODERATE"
    else:
        return "LOW"

df["risk"] = df["score"].apply(risk_level)

# -----------------------------
# METRICS
# -----------------------------
high = int(sum(df["risk"] == "HIGH"))
moderate = int(sum(df["risk"] == "MODERATE"))
low = int(sum(df["risk"] == "LOW"))

col1, col2, col3 = st.columns(3)
col1.metric("High Risk", high)
col2.metric("Moderate Risk", moderate)
col3.metric("Low Risk", low)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Risk Intelligence Table")
st.dataframe(df)

# -----------------------------
# CHART
# -----------------------------
st.subheader("📈 Risk Distribution")

fig, ax = plt.subplots()
ax.bar(["High", "Moderate", "Low"], [high, moderate, low])
ax.set_ylabel("Count")
ax.set_title(f"Risk Profile - {country}")

st.pyplot(fig)

# -----------------------------
# AI INSIGHT (SMARTER)
# -----------------------------
st.subheader("🤖 AI Insight Engine")

total_risk = high * 3 + moderate * 2 + low * 1

if high > 0:
    st.error("🚨 CRITICAL: High-risk health security threat detected.")
elif moderate >= 2:
    st.warning("⚠️ ELEVATED: Multiple moderate risks detected. Monitor closely.")
elif total_risk > 5:
    st.info("ℹ️ WATCH: Some risk activity detected, but stable overall.")
else:
    st.success("✅ STABLE: No significant health security threats detected.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("v3 - AI-assisted Global Health Intelligence System")
