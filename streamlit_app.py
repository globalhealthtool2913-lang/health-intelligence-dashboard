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
# 🧠 5 STEP ENTERPRISE ROADMAP
# =========================================

st.subheader("🧠 Enterprise Upgrade Roadmap (Your Next Steps)")

steps = [
    "1️⃣ Replace simulation with REAL WHO + GDELT live API ingestion",
    "2️⃣ Build FastAPI backend microservices architecture",
    "3️⃣ Add Kafka real-time streaming pipeline",
    "4️⃣ Integrate ML forecasting (outbreak prediction model)",
    "5️⃣ Deploy full system on AWS (Docker + CI/CD + monitoring)"
]

for s in steps:
    st.write(s)

st.divider()

# =========================================
# SIMULATED GLOBAL DATA (CURRENT SYSTEM)
# =========================================

def get_data():

    return [
        {"country": "Ethiopia", "cases": 2983, "deaths": 68, "risk": "MODERATE", "prediction": "STABLE", "source": "WHO"},
        {"country": "India", "cases": 5230, "deaths": 112, "risk": "HIGH", "prediction": "SPREADING", "source": "GDELT"},
        {"country": "Brazil", "cases": 7120, "deaths": 201, "risk": "HIGH", "prediction": "OUTBREAK LIKELY", "source": "WHO"},
        {"country": "Kenya", "cases": 1200, "deaths": 30, "risk": "LOW", "prediction": "STABLE", "source": "WHO"},
        {"country": "USA", "cases": 8450, "deaths": 310, "risk": "HIGH", "prediction": "SPREADING", "source": "GDELT"}
    ]

df = pd.DataFrame(get_data())

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
# GLOBAL DASHBOARD
# =========================================

st.subheader("🌍 Global Surveillance Dashboard")

st.dataframe(df, use_container_width=True)

st.divider()

# =========================================
# CLEAN RISK DISTRIBUTION
# =========================================

st.subheader("🚨 Risk Distribution")

risk_counts = df["risk"].value_counts()

risk_df = risk_counts.reset_index()
risk_df.columns = ["Risk Level", "Count"]

col1, col2 = st.columns(2)

with col1:
    st.write("📊 Table View")
    st.dataframe(risk_df, use_container_width=True)

with col2:
    st.write("📈 Chart View")
    st.bar_chart(risk_df.set_index("Risk Level"))

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
# LIVE STREAM SIMULATION
# =========================================

st.subheader("🔄 Live Global Stream")

container = st.container()

for _, row in df.iterrows():

    with container:

        st.write(
            f"🌍 **{row['country']}** | "
            f"📊 Cases: {row['cases']} | "
            f"⚰️ Deaths: {row['deaths']} | "
            f"🚨 Risk: {row['risk']} | "
            f"🧠 Prediction: {row['prediction']} | "
            f"📡 Source: {row['source']}"
        )

    time.sleep(0.25)

st.divider()

# =========================================
# FOOTER AUTO REFRESH
# =========================================

time.sleep(5)
st.rerun()
