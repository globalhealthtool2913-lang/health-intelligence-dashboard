import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v9",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v9")
st.caption("AI-assisted health surveillance & early warning system")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Surveillance Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Active monitoring region: {country}")

# -----------------------------
# DATA
# -----------------------------
data = [
    {"event": "Conflict-related disruption", "type": "conflict"},
    {"event": "Infectious disease signals", "type": "outbreak"},
    {"event": "Maternal & child health trends", "type": "child"},
    {"event": "Health system capacity stress", "type": "system"},
    {"event": "Vaccination coverage changes", "type": "system"}
]

df = pd.DataFrame(data)

# -----------------------------
# COUNTRY RISK MODEL (V9 CLEANER)
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

def classify(x):
    if x >= 70:
        return "HIGH"
    elif x >= 40:
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
# ALERT SYSTEM (CLEAN V9)
# -----------------------------
if high >= 2:
    st.error("🔴 CRITICAL ALERT: Immediate health security risk detected")
elif moderate >= 3:
    st.warning("🟠 ELEVATED ALERT: Increased surveillance required")
else:
    st.success("🟢 STABLE: No major health security threats detected")

# -----------------------------
# TABLE (CLEAN)
# -----------------------------
st.subheader("📊 Surveillance Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# VISUALIZATION (SIMPLE + STABLE)
# -----------------------------
st.subheader("📈 Risk Overview")

chart = pd.DataFrame({
    "Risk Level": ["High", "Moderate", "Low"],
    "Count": [high, moderate, low]
})

st.bar_chart(chart.set_index("Risk Level"))

# -----------------------------
# AI SITUATION REPORT (V9 IMPROVED)
# -----------------------------
st.subheader("🧠 AI Situation Report")

risk_score = high * 3 + moderate * 2 + low

if high > 0:
    status = "High-risk signals detected requiring urgent monitoring."
elif moderate >= 2:
    status = "Moderate risk activity detected requiring close surveillance."
else:
    status = "Low risk environment with stable indicators."

report = f"""
**Country:** {country}

**Summary:**
- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

**Assessment:**
{status}

**Recommendation:**
{'Activate emergency surveillance protocols.' if high >= 2 else 'Increase monitoring frequency and field reporting.' if moderate >= 2 else 'Maintain routine surveillance operations.'}
"""

st.markdown(report)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("v9 - Clean AI Health Intelligence Dashboard")
