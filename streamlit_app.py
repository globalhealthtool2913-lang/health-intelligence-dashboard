import streamlit as st
import pandas as pd
import time

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="WHO AI Enterprise Intelligence Platform",
    page_icon="🌍",
    layout="wide"
)

# =========================================
# HEADER
# =========================================

st.title("🌍 WHO AI Enterprise Intelligence Platform")
st.caption("FREE Streamlit Cloud Version (Stable Simulation Mode)")

# =========================================
# SIMULATED GLOBAL DATA
# =========================================

def get_data():

    return [
        {"country": "Ethiopia", "cases": 2983, "deaths": 68, "risk": "MODERATE", "prediction": "STABLE", "source": "WHO"},
        {"country": "India", "cases": 5230, "deaths": 112, "risk": "HIGH", "prediction": "SPREADING", "source": "GDELT"},
        {"country": "Brazil", "cases": 7120, "deaths": 201, "risk": "HIGH", "prediction": "OUTBREAK LIKELY", "source": "WHO"},
        {"country": "Kenya", "cases": 1200, "deaths": 30, "risk": "LOW", "prediction": "STABLE", "source": "WHO"},
        {"country": "USA", "cases": 8450, "deaths": 310, "risk": "HIGH", "prediction": "SPREADING", "source": "GDELT"}
    ]

data = get_data()
df = pd.DataFrame(data)

# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Live Events", len(df))
col2.metric("System Status", "ACTIVE")
col3.metric("Architecture", "SIMULATED")
col4.metric("AI Engine", "READY")

# =========================================
# GLOBAL DASHBOARD
# =========================================

st.subheader("🌍 Global Surveillance Dashboard")

st.dataframe(df, use_container_width=True)

# =========================================
# CLEAN RISK DISTRIBUTION (FIXED BUG)
# =========================================

st.subheader("🚨 Risk Distribution")

risk_counts = df["risk"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Count"]

st.bar_chart(risk_counts.set_index("Risk Level"))

# =========================================
# COUNTRY INTELLIGENCE
# =========================================

st.subheader("🌍 Country Intelligence")

country_stats = df.groupby("country")[["cases", "deaths"]].sum()

st.dataframe(country_stats, use_container_width=True)

# =========================================
# AI EPIDEMIOLOGY ENGINE PANEL
# =========================================

st.subheader("🧠 WHO AI Epidemiology Engine")

latest = df.iloc[-1]

st.info(
    f"""
🌍 Country: {latest['country']}

📊 Cases: {latest['cases']}

⚰️ Deaths: {latest['deaths']}

🚨 Risk Level: {latest['risk']}

📡 Source: {latest['source']}

🧠 Prediction: {latest['prediction']}
"""
)

# =========================================
# LIVE STREAM SIMULATION
# =========================================

st.subheader("🔄 Live Global Stream")

placeholder = st.empty()

for i in range(len(df)):

    item = df.iloc[i]

    with placeholder.container():

        st.write(
            f"🌍 **{item['country']}** | "
            f"📊 Cases: {item['cases']} | "
            f"⚰️ Deaths: {item['deaths']} | "
            f"🚨 Risk: {item['risk']} | "
            f"🧠 Prediction: {item['prediction']} | "
            f"📡 Source: {item['source']}"
        )

    time.sleep(0.3)

# =========================================
# AUTO REFRESH
# =========================================

time.sleep(6)
st.rerun()
    
