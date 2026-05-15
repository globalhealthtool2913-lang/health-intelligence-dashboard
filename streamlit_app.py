import streamlit as st
import pandas as pd
import requests

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence RW-4", layout="wide")

st.title("🌍 Global Health Intelligence System (RW-4)")
st.caption("Advanced intelligence prototype with map + scoring + reporting")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# INTELLIGENCE LAYER (SIMULATED REAL FEED)
# -----------------------------
def get_data():
    try:
        requests.get("https://api.reliefweb.int/v1/reports?appname=health-intel", timeout=5)

        return pd.DataFrame([
            {"event": "Cholera outbreak spreading rapidly", "country": "Ethiopia"},
            {"event": "Floods disrupting hospitals and clinics", "country": "Kenya"},
            {"event": "Armed conflict limiting healthcare access", "country": "Sudan"},
            {"event": "Malaria surge in rural districts", "country": "Somalia"},
            {"event": "Severe food insecurity affecting children", "country": "South Sudan"}
        ])
    except:
        return pd.DataFrame([
            {"event": "Disease outbreak reported", "country": "Ethiopia"},
            {"event": "Health system disruption", "country": "Kenya"},
            {"event": "Emergency response needed", "country": "Sudan"},
            {"event": "Public health stress detected", "country": "Somalia"},
            {"event": "Nutrition crisis escalating", "country": "South Sudan"}
        ])

df = get_data()
df = df[df["country"] == country]

# -----------------------------
# AI SCORING ENGINE (IMPROVED)
# -----------------------------
def score_risk(text):
    text = text.lower()

    score = 0

    high = ["cholera", "outbreak", "epidemic", "surge"]
    moderate = ["conflict", "flood", "malaria", "food", "displacement", "health system"]

    for w in high:
        if w in text:
            score += 2

    for w in moderate:
        if w in text:
            score += 1

    return score

df["score"] = df["event"].apply(score_risk)

def classify(score):
    if score >= 3:
        return "HIGH"
    elif score == 2:
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
# MAP INTELLIGENCE VIEW (SIMULATED HEAT)
# -----------------------------
st.subheader("🗺️ Regional Risk Intelligence Map")

map_data = pd.DataFrame({
    "lat": [9.1, 1.2, 15.6, 5.1, -1.2],
    "lon": [40.4, 36.8, 32.5, 46.2, 36.8],
    "country": ["Ethiopia", "Kenya", "Sudan", "Somalia", "Kenya"],
    "risk": [high, moderate, high, moderate, low]
})

st.map(map_data)

# -----------------------------
# ALERT ENGINE
# -----------------------------
if high >= 1:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL PUBLIC HEALTH RISK")
elif moderate >= 1:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")
else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# AI REPORT ENGINE (RW-4 STYLE)
# -----------------------------
st.subheader("🧠 AI Policy Brief")

st.write(f"""
### Executive Summary
Country: **{country}**
Risk Level: **{alert}**

### Situation Analysis
The system identifies a **{alert.lower()}-level health environment** based on structured intelligence signals.

### Key Drivers
- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

### Recommendation
{"Immediate emergency response activation required." if alert=="CRITICAL"
 else "Strengthen surveillance and field reporting." if alert=="ELEVATED"
 else "Maintain routine monitoring systems."}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-4 - Advanced Global Health Intelligence Prototype")
