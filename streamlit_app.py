import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard")
st.markdown("AI-powered monitoring for global health risks and alerts")

# -----------------------------
# COUNTRY SELECTOR
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
    {"title": "Conflict impacts health services"},
    {"title": "Disease outbreak monitoring"},
    {"title": "Child health progress"},
    {"title": "Health system strengthening"}
]

df = pd.DataFrame(data)

# -----------------------------
# RISK ENGINE
# -----------------------------
def score(text):
    text = text.lower()
    s = 0
    if "conflict" in text:
        s += 35
    if "outbreak" in text:
        s += 35
    if "child" in text:
        s += 20
    if "health" in text:
        s += 10
    return s

df["score"] = df["title"].apply(score)

def level(x):
    if x >= 60:
        return "HIGH"
    elif x >= 35:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(level)

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

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
# SAFE VISUALIZATION (NO BUGS)
# -----------------------------
st.subheader("📈 Risk Distribution")

st.write("High Risk Level:", "█" * high)
st.write("Moderate Risk Level:", "█" * moderate)
st.write("Low Risk Level:", "█" * low)

# -----------------------------
# AI INSIGHT
# -----------------------------
st.subheader("🤖 AI Insight Engine")

total = high * 3 + moderate * 2 + low

if high > 0:
    st.error("🚨 CRITICAL: High-risk health threat detected.")
elif moderate >= 2:
    st.warning("⚠️ ELEVATED: Multiple moderate risks detected.")
else:
    st.success("✅ STABLE: No major health threats detected.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Global Health Intelligence System (Stable Build)")
