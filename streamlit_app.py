import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v7",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v7")
st.markdown("AI-driven surveillance, risk analysis & early warning system")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Active monitoring zone: {country}")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"event": "Conflict disruption", "type": "conflict"},
    {"event": "Disease outbreak signals", "type": "outbreak"},
    {"event": "Child health trends", "type": "child"},
    {"event": "Health system capacity", "type": "system"},
    {"event": "Vaccination coverage shift", "type": "system"}
]

df = pd.DataFrame(data)

# -----------------------------
# COUNTRY INTELLIGENCE MODEL (V7)
# -----------------------------
risk_weights = {
    "Ethiopia": {"conflict": 1.0, "outbreak": 1.0, "child": 0.9, "system": 0.9},
    "Kenya": {"conflict": 0.8, "outbreak": 0.9, "child": 0.85, "system": 0.9},
    "Sudan": {"conflict": 1.3, "outbreak": 1.2, "child": 1.1, "system": 1.0},
    "Somalia": {"conflict": 1.4, "outbreak": 1.3, "child": 1.2, "system": 1.1},
    "South Sudan": {"conflict": 1.5, "outbreak": 1.4, "child": 1.3, "system": 1.2}
}

weights = risk_weights[country]

# -----------------------------
# RISK ENGINE
# -----------------------------
base = {
    "conflict": 45,
    "outbreak": 45,
    "child": 25,
    "system": 15
}

def compute(row):
    return base[row["type"]] * weights[row["type"]]

df["score"] = df.apply(compute, axis=1)

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
col1.metric("🔴 High Risk", high)
col2.metric("🟠 Moderate Risk", moderate)
col3.metric("🟢 Low Risk", low)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df)

# -----------------------------
# ALERT LEVEL SYSTEM (NEW V7)
# -----------------------------
st.subheader("🚨 Alert Status")

if high >= 2:
    alert = "🔴 RED ALERT"
    st.error("Critical instability detected. Immediate intervention required.")
elif moderate >= 3:
    alert = "🟠 YELLOW ALERT"
    st.warning("Elevated risk environment detected. Close monitoring required.")
else:
    alert = "🟢 GREEN STATUS"
    st.success("Stable surveillance environment. No immediate threats.")

st.markdown(f"### Current Status: {alert}")

# -----------------------------
# AI REPORT ENGINE (V7 KEY FEATURE)
# -----------------------------
st.subheader("🤖 AI Situation Report")

report = f"""
**Country:** {country}

**Summary:**
- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

**Interpretation:**
The system indicates a {'high' if high > 0 else 'moderate' if moderate > 2 else 'low'} level of health security concern in {country}.

**Recommendation:**
{'Immediate response and field investigation required.' if high >= 2 else 'Increase surveillance and monitor trends closely.' if moderate >= 2 else 'Maintain routine monitoring.'}
"""

st.markdown(report)

# -----------------------------
# SIMPLE VISUALIZATION (STABLE)
# -----------------------------
st.subheader("📈 Risk Overview")

chart = pd.DataFrame({
    "Category": ["High", "Moderate", "Low"],
    "Score": [high * 3, moderate * 2, low]
})

st.line_chart(chart.set_index("Category"))

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("v7 - AI-enhanced Global Health Intelligence System")
