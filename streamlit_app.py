import streamlit as st
import pandas as pd
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence RW-2",
    layout="wide"
)

st.title("🌍 Global Health Intelligence System (RW-2)")
st.caption("Real-world inspired outbreak intelligence prototype")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring region: {country}")

# -----------------------------
# LIVE / SIMULATED DATA LAYER
# -----------------------------
def get_live_data():
    try:
        # Example external API structure (fallback-safe)
        url = "https://api.reliefweb.int/v1/reports?appname=health-intel"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return pd.DataFrame([
                {"event": "Disease outbreak reported in East Africa", "country": "Ethiopia"},
                {"event": "Flooding disrupting health services", "country": "Kenya"},
                {"event": "Conflict affecting hospital access", "country": "Sudan"},
                {"event": "Vaccination disruption in rural areas", "country": "Somalia"}
            ])
    except:
        pass

    # fallback dataset (always works)
    return pd.DataFrame([
        {"event": "Cholera outbreak reported in flood region", "country": "Ethiopia"},
        {"event": "Measles cases rising in displacement camps", "country": "Sudan"},
        {"event": "Health facility disruption due to conflict", "country": "Somalia"},
        {"event": "Food insecurity affecting children", "country": "South Sudan"},
        {"event": "Malaria surge during rainy season", "country": "Kenya"}
    ])

df = get_live_data()

# Filter by country
df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE (REAL WORLD STYLE)
# -----------------------------
def detect_risk(text):
    text = text.lower()

    high_keywords = ["cholera", "outbreak", "epidemic", "measles", "surge"]
    moderate_keywords = ["conflict", "flood", "displacement", "shortage", "food", "malaria"]

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
    st.warning("⚠️ ELEVATED ALERT: Multiple regional risk signals detected")
else:
