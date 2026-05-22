import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px

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
st.markdown("Next-Gen Global Epidemic Intelligence Platform")

# =========================
# FETCH DATA
# =========================

def fetch_data():
    try:
        res = requests.get(f"{API_BASE}/events")
        return res.json()
    except:
        return []

data = fetch_data()

df = pd.DataFrame(data) if data else pd.DataFrame()

# =========================
# KPI SECTION
# =========================

st.subheader("📊 Global Outbreak Overview")

if not df.empty:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", len(df))
    col2.metric("Latest Country", df.iloc[-1]["country"])
    col3.metric("Max Cases", df["cases"].max())
    col4.metric("Max Deaths", df["deaths"].max())

else:
    st.warning("No data available from backend")

# =========================
# 🌍 GLOBAL HEATMAP (SIMULATED)
# =========================

st.subheader("🌍 Global Outbreak Heatmap")

if not df.empty:

    # Simple mapping (expandable to real geo later)
    country_map = {
        "Ethiopia": [9.03, 38.74],
        "Kenya": [-1.29, 36.82],
        "Nigeria": [9.08, 8.67],
        "India": [20.59, 78.96],
        "Brazil": [-14.23, -51.92]
    }

    df["lat"] = df["country"].apply(lambda x: country_map.get(x, [0,0])[0])
    df["lon"] = df["country"].apply(lambda x: country_map.get(x, [0,0])[1])

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size="cases",
        color="deaths",
        hover_name="country",
        title="Global Outbreak Intensity Map"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🔔 SMART ALERT SYSTEM
# =========================

st.subheader("🔔 Smart Risk Alerts")

if not df.empty:

    alerts = df[df["cases"] > 2500]

    if not alerts.empty:

        for _, row in alerts.iterrows():

            st.error(
                f"⚠️ HIGH RISK: {row['country']} | "
                f"Cases: {row['cases']} | "
                f"Deaths: {row['deaths']}"
            )

    else:
        st.success("No high-risk outbreaks detected")

# =========================
# 🧠 GPT EPIDEMIOLOGY BRAIN
# =========================

st.subheader("🧠 AI Epidemiology Brain")

if not df.empty:

    latest = df.iloc[-1]

    cases = latest["cases"]
    deaths = latest["deaths"]

    mortality = round((deaths / cases) * 100, 2)

    if cases > 4000:
        spread = "Very High Transmission"
    elif cases > 2000:
        spread = "Moderate Transmission"
    else:
        spread = "Controlled Spread"

    if mortality > 5:
        severity = "Severe"
    elif mortality > 2:
        severity = "Moderate"
    else:
        severity = "Low"

    st.info(f"""
### WHO AI ANALYSIS REPORT

Country: {latest['country']}

Transmission Level: {spread}

Severity Level: {severity}

Mortality Rate: {mortality}%

### Interpretation:
This outbreak shows {spread.lower()} dynamics with {severity.lower()} clinical impact.
Recommend enhanced surveillance and regional coordination.
""")

# =========================
# 📈 PREDICTION ENGINE (SIMPLE AI MODEL)
# =========================

st.subheader("📈 Outbreak Risk Prediction Engine")

if not df.empty:

    df["risk_score"] = (df["cases"] * 0.7) + (df["deaths"] * 2)

    top_risk = df.sort_values("risk_score", ascending=False).head(5)

    st.write("Top 5 High-Risk Regions:")

    st.dataframe(top_risk)

# =========================
# 🌐 LIVE FEED
# =========================

st.subheader("🌐 Live Outbreak Feed")

if not df.empty:

    for _, row in df.tail(10).iterrows():

        st.warning(
            f"{row['country']} | Cases: {row['cases']} | Deaths: {row['deaths']}"
        )

# =========================
# AUTO REFRESH
# =========================

time.sleep(10)
st.rerun()
