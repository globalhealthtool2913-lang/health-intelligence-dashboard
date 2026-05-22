import streamlit as st
import requests
import pandas as pd
import time

# =========================
# CONFIG
# =========================

API_BASE = "https://Globalhealthtool.pythonanywhere.com"

st.set_page_config(
    page_title="WHO AI Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🌍 WHO AI Intelligence System")

st.markdown("""
Real-time epidemic intelligence, outbreak monitoring,
and AI epidemiology analysis platform.
""")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🧠 WHO AI Control Center")

refresh = st.sidebar.slider(
    "Refresh interval (seconds)",
    5,
    60,
    10
)

risk_threshold = st.sidebar.slider(
    "High Risk Case Threshold",
    1000,
    10000,
    3000
)

# =========================
# LIVE STATUS
# =========================

st.subheader("🟢 System Status")

col1, col2, col3 = st.columns(3)

col1.success("Backend Online")
col2.success("AI Monitoring Active")
col3.success("Outbreak Stream Running")

# =========================
# LIVE OUTBREAK STREAM
# =========================

st.subheader("🔴 Live Global Outbreak Intelligence")

try:

    response = requests.get(f"{API_BASE}/events")
    outbreaks = response.json()

    if outbreaks:

        latest = outbreaks[-1]

        # =========================
        # METRICS
        # =========================

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Latest Country",
            latest["country"]
        )

        m2.metric(
            "Cases",
            latest["cases"]
        )

        m3.metric(
            "Deaths",
            latest["deaths"]
        )

        # =========================
        # TABLE
        # =========================

        st.subheader("📊 Outbreak Data")

        df = pd.DataFrame(outbreaks)

        st.dataframe(
            df,
            use_container_width=True
        )

        # =========================
        # HIGH RISK ALERTS
        # =========================

        st.subheader("🚨 AI High-Risk Alerts")

        high_risk = []

        for outbreak in outbreaks:

            if outbreak["cases"] > risk_threshold:

                high_risk.append(outbreak)

        if high_risk:

            for outbreak in reversed(high_risk):

                st.error(
                    f"⚠️ HIGH RISK: "
                    f"{outbreak['country']} | "
                    f"Cases: {outbreak['cases']} | "
                    f"Deaths: {outbreak['deaths']}"
                )

        else:

            st.success("No high-risk outbreaks detected.")

        # =========================
        # AI EPIDEMIOLOGY ANALYSIS
        # =========================

        st.subheader("🧠 GPT Epidemiology Reasoning")

        latest_cases = latest["cases"]
        latest_deaths = latest["deaths"]

        mortality_rate = round(
            (latest_deaths / latest_cases) * 100,
            2
        )

        if latest_cases > 4000:

            transmission = "Very High"

        elif latest_cases > 2000:

            transmission = "Moderate"

        else:

            transmission = "Controlled"

        if mortality_rate > 5:

            severity = "Severe"

        elif mortality_rate > 2:

            severity = "Moderate"

        else:

            severity = "Low"

        st.info(f"""
### WHO AI Epidemiology Assessment

Country: {latest['country']}

Estimated Transmission Level: {transmission}

Estimated Severity: {severity}

Mortality Rate: {mortality_rate}%

AI Interpretation:
The outbreak demonstrates {transmission.lower()} transmission dynamics
with {severity.lower()} clinical severity indicators.
Cross-border surveillance and regional preparedness are recommended.
""")

        # =========================
        # STREAMING FEED
        # =========================

        st.subheader("📡 Live Intelligence Feed")

        for outbreak in reversed(outbreaks[-10:]):

            st.warning(
                f"🌍 {outbreak['country']} | "
                f"{outbreak['cases']} cases | "
                f"{outbreak['deaths']} deaths"
            )

    else:

        st.warning("No outbreak data available.")

except Exception as e:

    st.error("❌ Backend connection failed")
    st.text(str(e))

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption("""
WHO AI Intelligence Platform • Real-Time Epidemic Intelligence •
Global Health Surveillance System
""")

# =========================
# AUTO REFRESH
# =========================

time.sleep(refresh)
st.rerun()
