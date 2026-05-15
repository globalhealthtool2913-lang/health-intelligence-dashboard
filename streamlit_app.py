import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence - Real World Mode",
    layout="wide"
)

st.title("🌍 Global Health Intelligence System (Real World Mode)")
st.caption("AI-assisted outbreak monitoring & early warning system")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring region: {country}")

# -----------------------------
# REAL-WORLD STYLE DATA (SIMULATED SOURCES)
# -----------------------------
def get_data():
    return pd.DataFrame([
        {"event": "Cholera outbreak reported in flood-affected region", "country": "Ethiopia"},
        {"event": "Measles cases rising in displacement camps", "country": "Sudan"},
        {"event": "Health facility disruption due to conflict", "country": "Somalia"},
        {"event": "Vaccination coverage decline in rural areas", "country": "Kenya"},
        {"event": "Malaria surge during rainy season", "country": "Ethiopia"},
        {"event": "Food insecurity affecting child nutrition", "country": "South Sudan"}
    ])

df = get_data()

# Filter by country
df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE (REAL WORLD STYLE NLP RULES)
# -----------------------------
def detect_risk(text):
    text = text.lower()

    high_keywords = ["cholera", "outbreak", "epidemic", "measles", "surge"]
    moderate_keywords = ["conflict", "displacement", "flood", "shortage", "food insecurity", "malaria"]

    if any(word in text for word in high_keywords):
        return "HIGH"
    elif any(word in text for word in moderate_keywords):
        return "MODERATE"
    else:
        return "LOW"

df["risk"] = df["event"].apply(detect_risk)

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
# ALERT SYSTEM
# -----------------------------
if high >= 2:
    st.error("🚨 CRITICAL ALERT: High-confidence outbreak signals detected")
elif moderate >= 3:
    st.warning("⚠️ ELEVATED ALERT: Multiple risk signals detected")
else:
    st.success("🟢 STABLE: No major public health threats detected")

# -----------------------------
# AI SITUATION REPORT
# -----------------------------
st.subheader("🧠 Situation Report")

if high > 0:
    status = "High-risk public health threats detected requiring immediate attention."
elif moderate > 0:
    status = "Moderate risk signals detected. Enhanced surveillance recommended."
else:
    status = "Stable public health conditions."

st.write(f"""
**Country:** {country}

**Summary:**
- High risk signals: {high}
- Moderate risk signals: {moderate}
- Low risk signals: {low}

**Assessment:**
{status}

**Recommendation:**
{'Activate emergency response protocols.' if high >= 2 else 'Increase surveillance and field reporting.' if moderate > 0 else 'Maintain routine monitoring.'}
""")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Real World Mode - Global Health Intelligence Prototype")
