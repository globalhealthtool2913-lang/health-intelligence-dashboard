import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v5",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v5")
st.markdown("Advanced AI-assisted global health risk monitoring system")

# -----------------------------
# COUNTRY CONTEXT
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Analyzing health security signals for: {country}")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"title": "Conflict impacts health services", "type": "conflict"},
    {"title": "Disease outbreak monitoring", "type": "outbreak"},
    {"title": "Child health progress", "type": "child"},
    {"title": "Health system strengthening", "type": "system"}
]

df = pd.DataFrame(data)

# -----------------------------
# COUNTRY RISK FACTOR (NEW IN V5)
# -----------------------------
country_factor = {
    "Ethiopia": 1.0,
    "Kenya": 0.9,
    "Sudan": 1.2,
    "Somalia": 1.3,
    "South Sudan": 1.4
}

factor = country_factor[country]

# -----------------------------
# IMPROVED RISK ENGINE
# -----------------------------
def risk_score(t):
    base = {
        "conflict": 35,
        "outbreak": 35,
        "child": 20,
        "system": 10
    }
    return base.get(t, 5) * factor

df["score"] = df["type"].apply(risk_score)

def classify(x):
    if x >= 60:
        return "HIGH"
    elif x >= 35:
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
col1.metric("High Risk", high)
col2.metric("Moderate Risk", moderate)
col3.metric("Low Risk", low)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Risk Intelligence Table")
st.dataframe(df)

# -----------------------------
# CHART (STABLE + CLEAN)
# -----------------------------
st.subheader("📈 Risk Distribution")

chart = pd.DataFrame({
    "Risk": ["High", "Moderate", "Low"],
    "Count": [high, moderate, low]
})

st.bar_chart(chart.set_index("Risk"))

# -----------------------------
# SMART AI INSIGHT (V5)
# -----------------------------
st.subheader("🤖 AI Insight Engine")

risk_total = (high * 3 + moderate * 2 + low)

if high > 0:
    st.error(
        f"🚨 HIGH ALERT in {country}: "
        "Critical health security risks detected. Immediate monitoring required."
    )
elif moderate >= 2:
    st.warning(
        f"⚠️ ELEVATED RISK in {country}: "
        "Multiple moderate signals detected. Increased surveillance recommended."
    )
elif risk_total > 6:
    st.info(
        f"ℹ️ WATCHLIST {country}: "
        "Some risk activity present, but system remains stable."
    )
else:
    st.success(
        f"✅ STABLE {country}: No significant health threats detected."
    )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("v5 - AI-enhanced Global Health Intelligence System")
