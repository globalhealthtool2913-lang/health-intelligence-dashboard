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
st.caption("Stable Simulation Mode (Streamlit Cloud Ready)")

st.divider()

# =========================================
# SIMULATED DATA (SAFE FOR STREAMLIT CLOUD)
# =========================================

def load_data():

    return [
        {"country": "Ethiopia", "cases": 2983, "deaths": 68, "risk": "MODERATE", "prediction": "STABLE", "source": "WHO"},
        {"country": "India", "cases": 5230, "deaths": 112, "risk": "HIGH", "prediction": "SPREADING", "source": "GDELT"},
        {"country": "Brazil", "cases": 7120, "deaths": 201, "risk": "HIGH", "prediction": "OUTBREAK LIKELY", "source": "WHO"},
        {"country": "Kenya", "cases": 1200, "deaths": 30, "risk": "LOW", "prediction": "STABLE", "source": "WHO"},
        {"country": "USA", "cases": 8450, "deaths": 310, "risk": "HIGH", "prediction": "SPREADING", "source": "GDELT"}
    ]

data = load_data()
df = pd.DataFrame(data)

# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Live Events", len(df))
col2.metric("System Status", "ACTIVE")
col3.metric("Architecture", "SIMULATED")
col4.metric("AI Engine", "READY")

st.divider()

# =========================================
# GLOBAL TABLE
# =========================================

st.subheader("🌍 Global Surveillance Dashboard")

st.dataframe(df, use_container_width=True)

st.divider()

# =========================================
# CLEAN RISK DISTRIBUTION (FIXED)
# =========================================

st.subheader("🚨 Risk Distribution")

risk_counts = df["risk"].value_counts()

st.dataframe(risk_counts)

st.bar_chart(risk_counts)

st.divider()

# =========================================
# COUNTRY INTELLIGENCE
# =========================================

st.subheader("🌍 Country Intelligence")

country_stats = df.groupby("country")[["cases", "deaths"]].sum()

st.dataframe(country_stats, use_container_width=True)

st.divider()

# =========================================
# AI EPIDEMIOLOGY ENGINE
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

st.divider()

# =========================================
# LIVE STREAM (CLEAN + FIXED)
# =========================================

st.subheader("🔄 Live Global Stream")

stream_placeholder = st.container()

for _, row in df.iterrows():

    with stream_placeholder:

        st.write(
            f"🌍 **{row['country']}** | "
            f"📊 Cases: {row['cases']} | "
            f"⚰️ Deaths: {row['deaths']} | "
            f"🚨 Risk: {row['risk']} | "
            f"🧠 Prediction: {row['prediction']} | "
            f"📡 Source: {row['source']}"
        )

    time.sleep(0.3)

st.divider()

# =========================================
# FOOTER AUTO REFRESH
# =========================================

time.sleep(5)
st.rerun()
