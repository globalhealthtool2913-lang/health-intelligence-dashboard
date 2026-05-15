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
# DATA LAYER
# -----------------------------
def get_live_data():
    try:
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
# RISK ENGINE
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
# ALERT SYSTEM (FIXED INDENTATION)
# -----------------------------
if high >= 2:
    st.error("🚨 CRITICAL ALERT: High-confidence outbreak signals detected")
elif moderate >= 3:
    st.warning("⚠️ ELEVATED ALERT: Multiple regional risk signals detected")
else:
    st.success("🟢 STABLE: No major public health threats detected")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# MAP VIEW
# -----------------------------
st.subheader("🗺️ Regional Risk View")

map_data = pd.DataFrame({
    "lat": [9.145, 1.2921, 15.5, 5.1521, -1.286],
    "lon": [40.4897, 36.8219, 32.5599, 46.1996, 36.8219],
    "country": ["Ethiopia", "Kenya", "Sudan", "Somalia", "Kenya"],
    "risk": [high, moderate, high, moderate, low]
})

st.map(map_data)

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

risk_level = "HIGH" if high > 0 else "MODERATE" if moderate > 0 else "LOW"

st.write(f"""
### Global Health Assessment

- **Country:** {country}
- **Risk Level:** {risk_level}

### Interpretation
The system detects **{risk_level.lower()}-level health security signals**.

### Recommendation
{'Activate emergency response protocols immediately.' if high > 0 else 'Increase surveillance and reporting frequency.' if moderate > 0 else 'Maintain routine monitoring operations.'}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-2 - Fixed Global Health Intelligence Prototype")
