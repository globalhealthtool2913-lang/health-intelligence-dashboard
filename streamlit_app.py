import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v6",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v6")
st.markdown("AI-driven health risk monitoring & early warning system")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Active surveillance region: {country}")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"event": "Conflict disruption", "type": "conflict"},
    {"event": "Infectious disease outbreak", "type": "outbreak"},
    {"event": "Maternal & child health progress", "type": "child"},
    {"event": "Health system resilience", "type": "system"},
    {"event": "Vaccination coverage change", "type": "system"}
]

df = pd.DataFrame(data)

# -----------------------------
# COUNTRY RISK PROFILE (IMPROVED V6)
# -----------------------------
country_profile = {
    "Ethiopia": {"conflict": 1.0, "outbreak": 1.0, "child": 0.9, "system": 0.9},
    "Kenya": {"conflict": 0.8, "outbreak": 0.9, "child": 0.85, "system": 0.9},
    "Sudan": {"conflict": 1.3, "outbreak": 1.2, "child": 1.1, "system": 1.0},
    "Somalia": {"conflict": 1.4, "outbreak": 1.3, "child": 1.2, "system": 1.1},
    "South Sudan": {"conflict": 1.5, "outbreak": 1.4, "child": 1.3, "system": 1.2}
}

profile = country_profile[country]

# -----------------------------
# RISK ENGINE (IMPROVED LOGIC)
# -----------------------------
base_scores = {
    "conflict": 40,
    "outbreak": 40,
    "child": 25,
    "system": 15
}

def compute_score(t):
    return base_scores[t["type"]] * profile[t["type"]]

df["score"] = df.apply(compute_score, axis=1)

def classify(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
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
st.subheader("📊 Surveillance Intelligence Table")
st.dataframe(df)

# -----------------------------
# TREND-LIKE VISUALIZATION (V6 IMPROVEMENT)
# -----------------------------
st.subheader("📈 Risk Pattern Overview")

trend = pd.DataFrame({
    "Category": ["High", "Moderate", "Low"],
    "Score": [high * 3, moderate * 2, low]
})

st.line_chart(trend.set_index("Category"))

# -----------------------------
# AI INSIGHT ENGINE (V6)
# -----------------------------
st.subheader("🤖 AI Insight Engine")

risk_index = (high * 3 + moderate * 2 + low) / len(df)

if high >= 2:
    st.error(f"🚨 CRITICAL ALERT in {country}: High-risk clustering detected. Immediate response required.")
elif moderate >= 3:
    st.warning(f"⚠️ ELEVATED ALERT in {country}: Multiple moderate signals indicate instability.")
elif risk_index > 2:
    st.info(f"ℹ️ WATCHLIST: {country} shows moderate surveillance signals.")
else:
    st.success(f"✅ STABLE: {country} shows low health security risk levels.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("v6 - Advanced AI Health Intelligence Prototype")
