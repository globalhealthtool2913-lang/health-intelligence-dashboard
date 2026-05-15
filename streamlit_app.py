import streamlit as st
import pandas as pd
import requests

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence RW-3", layout="wide")

st.title("🌍 Global Health Intelligence System (RW-3)")
st.caption("Real-time inspired outbreak intelligence + AI analysis layer")

# -----------------------------
# COUNTRY
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# LIVE NEWS INTELLIGENCE LAYER
# -----------------------------
def get_intelligence_data():
    try:
        # placeholder for real API (GDELT / ReliefWeb)
        url = "https://api.reliefweb.int/v1/reports?appname=health-intel"
        requests.get(url, timeout=5)

        return pd.DataFrame([
            {"event": "Cholera outbreak spreading in East Africa", "country": "Ethiopia"},
            {"event": "Floods disrupt hospital services", "country": "Kenya"},
            {"event": "Conflict escalates affecting health access", "country": "Sudan"},
            {"event": "Malaria surge reported in rural areas", "country": "Somalia"},
            {"event": "Food insecurity rising among children", "country": "South Sudan"}
        ])
    except:
        return pd.DataFrame([
            {"event": "Cholera outbreak detected", "country": "Ethiopia"},
            {"event": "Measles cases increasing", "country": "Sudan"},
            {"event": "Flooding affecting clinics", "country": "Kenya"},
            {"event": "Health system disruption", "country": "Somalia"},
            {"event": "Child malnutrition rising", "country": "South Sudan"}
        ])

df = get_intelligence_data()
df = df[df["country"] == country]

# -----------------------------
# AI RISK CLASSIFIER (IMPROVED)
# -----------------------------
def classify_risk(text):
    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "measles", "surge"]
    moderate = ["conflict", "flood", "displacement", "malaria", "food", "shortage"]

    if any(w in text for w in high):
        return "HIGH"
    elif any(w in text for w in moderate):
        return "MODERATE"
    return "LOW"

df["risk"] = df["event"].apply(classify_risk)

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

c1, c2, c3 = st.columns(3)
c1.metric("🔴 High", high)
c2.metric("🟠 Moderate", moderate)
c3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT ENGINE (RW-3 IMPROVED)
# -----------------------------
if high >= 2:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL OUTBREAK RISK DETECTED")
elif moderate >= 3:
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
# AI ANALYSIS ENGINE
# -----------------------------
st.subheader("🧠 AI Situation Report")

summary = f"""
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
"""

st.markdown(summary)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-3 - Real Intelligence Layer Prototype")
