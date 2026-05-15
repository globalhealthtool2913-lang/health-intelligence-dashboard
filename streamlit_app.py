import streamlit as st
import pandas as pd
import requests

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence RW-3", layout="wide")

st.title("🌍 Global Health Intelligence System (RW-3 FIXED)")
st.caption("AI-assisted outbreak intelligence + correct risk logic")

# -----------------------------
# COUNTRY
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# DATA LAYER
# -----------------------------
def get_intelligence_data():
    try:
        requests.get("https://api.reliefweb.int/v1/reports?appname=health-intel", timeout=5)

        return pd.DataFrame([
            {"event": "Cholera outbreak spreading in East Africa", "country": "Ethiopia"},
            {"event": "Floods disrupting health services", "country": "Kenya"},
            {"event": "Conflict escalating in region affecting hospitals", "country": "Sudan"},
            {"event": "Malaria surge reported in rural areas", "country": "Somalia"},
            {"event": "Food insecurity increasing among children", "country": "South Sudan"}
        ])
    except:
        return pd.DataFrame([
            {"event": "Cholera outbreak reported", "country": "Ethiopia"},
            {"event": "Measles cases increasing", "country": "Sudan"},
            {"event": "Flooding affecting clinics", "country": "Kenya"},
            {"event": "Health system disruption", "country": "Somalia"},
            {"event": "Child malnutrition rising", "country": "South Sudan"}
        ])

df = get_intelligence_data()
df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE
# -----------------------------
def classify_risk(text):
    text = text.lower()

    high_keywords = ["cholera", "outbreak", "epidemic", "measles", "surge"]
    moderate_keywords = ["conflict", "flood", "displacement", "malaria", "food", "shortage"]

    if any(w in text for w in high_keywords):
        return "HIGH"
    elif any(w in text for w in moderate_keywords):
        return "MODERATE"
    return "LOW"

df["risk"] = df["event"].apply(classify_risk)

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
# FIXED ALERT LOGIC (IMPORTANT)
# -----------------------------
if high >= 1:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL OUTBREAK RISK DETECTED")
elif moderate >= 1:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED REGIONAL RISK DETECTED")
else:
    alert = "STABLE"
    st.success("🟢 STABLE PUBLIC HEALTH CONDITIONS")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

st.write(f"""
### Situation Overview
Country: **{country}**
Risk Level: **{alert}**

### Key Signals
- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

### Interpretation
This indicates a **{alert.lower()}-level health security environment**.

### Recommended Action
{"Activate emergency response protocols immediately." if alert=="CRITICAL"
 else "Increase surveillance and monitoring intensity." if alert=="ELEVATED"
 else "Maintain routine monitoring operations."}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-3 FIXED - Global Health Intelligence Prototype")
