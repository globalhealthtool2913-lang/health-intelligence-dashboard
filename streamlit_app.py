import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v10",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v10")
st.caption("AI-powered global health surveillance & early warning system")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Surveillance Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring region: {country}")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"event": "Conflict disruption", "type": "conflict"},
    {"event": "Disease outbreak signals", "type": "outbreak"},
    {"event": "Maternal & child health trends", "type": "child"},
    {"event": "Health system pressure", "type": "system"},
    {"event": "Vaccination coverage shifts", "type": "system"}
]

df = pd.DataFrame(data)

# -----------------------------
# COUNTRY RISK MODEL
# -----------------------------
weights = {
    "Ethiopia": {"conflict": 1.0, "outbreak": 1.0, "child": 0.9, "system": 0.9},
    "Kenya": {"conflict": 0.8, "outbreak": 0.9, "child": 0.85, "system": 0.9},
    "Sudan": {"conflict": 1.3, "outbreak": 1.2, "child": 1.1, "system": 1.0},
    "Somalia": {"conflict": 1.4, "outbreak": 1.3, "child": 1.2, "system": 1.1},
    "South Sudan": {"conflict": 1.5, "outbreak": 1.4, "child": 1.3, "system": 1.2}
}

w = weights[country]

base = {
    "conflict": 45,
    "outbreak": 45,
    "child": 25,
    "system": 15
}

df["score"] = df["type"].apply(lambda x: base[x] * w[x])

def classify(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
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
col1.metric("🔴 High Risk", high)
col2.metric("🟠 Moderate Risk", moderate)
col3.metric("🟢 Low Risk", low)

st.divider()

# -----------------------------
# CLEAN ALERT SYSTEM
# -----------------------------
if high >= 2:
    st.error("🚨 CRITICAL ALERT: Immediate health security intervention required")
elif moderate >= 3:
    st.warning("⚠️ ELEVATED ALERT: Increased surveillance recommended")
else:
    st.success("🟢 STABLE: No major health threats detected")

# -----------------------------
# TABLE (CLEAN + PORTFOLIO STYLE)
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# VISUALIZATION (SIMPLE & RELIABLE)
# -----------------------------
st.subheader("📈 Risk Distribution")

chart = pd.DataFrame({
    "Risk": ["High", "Moderate", "Low"],
    "Count": [high, moderate, low]
})

st.bar_chart(chart.set_index("Risk"))

# -----------------------------
# AI REPORT (V10 IMPROVED)
# -----------------------------
st.subheader("🧠 AI Situation Report")

risk_level = "high" if high > 0 else "moderate" if moderate >= 2 else "low"

report = f"""
### Executive Summary
The surveillance system indicates a **{risk_level.upper()}-level** health security environment in **{country}**.

### Key Findings
- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

### Interpretation
This pattern suggests a **{risk_level} confidence risk environment**, requiring {'urgent intervention' if high >= 2 else 'enhanced monitoring' if moderate >= 2 else 'routine surveillance'}.

### Recommendation
{'Activate emergency response protocols and field verification.' if high >= 2 else 'Increase monitoring frequency and strengthen reporting systems.' if moderate >= 2 else 'Maintain routine surveillance operations.'}
"""

st.markdown(report)

# -----------------------------
# EXPORT READY FOOTER
# -----------------------------
st.markdown("---")
st.caption("v10 - Portfolio-ready Global Health Intelligence Dashboard")
