
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard")
st.markdown("AI-powered monitoring for health security risks and alerts")

# -----------------------------
# SAMPLE DATA
# -----------------------------
data = [
    {"title": "Conflict impacts health services", "category": "Conflict"},
    {"title": "Disease outbreak monitoring", "category": "Disease"},
    {"title": "Child health progress", "category": "Child Health"},
    {"title": "Health system strengthening", "category": "Routine"}
]

df = pd.DataFrame(data)

# -----------------------------
# RISK SCORING FUNCTION
# -----------------------------
def score_risk(text):
    text = text.lower()
    score = 0

    if "conflict" in text:
        score += 30
    if "outbreak" in text:
        score += 30
    if "child" in text:
        score += 15

    return score

df["score"] = df["title"].apply(score_risk)

def risk_level(score):
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MODERATE"
    else:
        return "LOW"

df["risk"] = df["score"].apply(risk_level)

# -----------------------------
# METRICS
# -----------------------------
high = sum(df["risk"] == "HIGH")
moderate = sum(df["risk"] == "MODERATE")
low = sum(df["risk"] == "LOW")

col1, col2, col3 = st.columns(3)
col1.metric("High Risk", high)
col2.metric("Moderate Risk", moderate)
col3.metric("Low Risk", low)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Risk Analysis Table")
st.dataframe(df)

# -----------------------------
# CHART
# -----------------------------
st.subheader("📈 Risk Distribution")

fig, ax = plt.subplots()
ax.bar(["High", "Moderate", "Low"], [high, moderate, low])
st.pyplot(fig)

# -----------------------------
# AI INSIGHT
# -----------------------------
st.subheader("🤖 AI Insight")

if high > 0:
    st.error("⚠️ High-risk signals detected. Immediate attention required.")
elif moderate > low:
    st.warning("⚠️ Moderate risk environment. Monitoring recommended.")
else:
    st.success("✅ Stable situation. No major risks detected.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Built for global health intelligence and early warning analysis")
