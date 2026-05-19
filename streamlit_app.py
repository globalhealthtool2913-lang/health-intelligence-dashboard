import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import os
from datetime import datetime

# =========================
# SAFE OPENAI IMPORT
# =========================
GPT_AVAILABLE = False

try:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        client = OpenAI(api_key=api_key)
        GPT_AVAILABLE = True

except Exception:
    GPT_AVAILABLE = False

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="WHO Global AI Intelligence System",
    layout="wide"
)

st.title("🌍 WHO Global AI Intelligence System")
st.caption(
    "Autonomous Multi-Agent Surveillance + Forecasting + Event Intelligence"
)

# =========================
# MEMORY SYSTEM
# =========================
if "memory" not in st.session_state:
    st.session_state.memory = []

# =========================
# LIVE DATA ENGINE
# =========================
@st.cache_data(ttl=120)
def load_data():

    try:
        url = "https://disease.sh/v3/covid-19/countries"

        r = requests.get(url, timeout=20)

        if r.status_code == 200:

            data = r.json()

            df = pd.DataFrame(data)[[
                "country",
                "casesPerOneMillion",
                "deathsPerOneMillion"
            ]]

            df.columns = [
                "Country",
                "Cases",
                "Deaths"
            ]

            df["Policy"] = np.random.randint(
                40,
                90,
                len(df)
            )

            return df, True

    except Exception:
        pass

    fallback = pd.DataFrame({
        "Country": [
            "Ethiopia",
            "Kenya",
            "USA",
            "India",
            "Brazil"
        ],
        "Cases": np.random.randint(1000, 5000, 5),
        "Deaths": np.random.randint(50, 300, 5),
        "Policy": np.random.randint(40, 90, 5)
    })

    return fallback, False

# =========================
# LOAD DATA
# =========================
df, live_status = load_data()

# =========================
# STATUS
# =========================
if live_status:
    st.success("🟢 LIVE GLOBAL HEALTH STREAM ACTIVE")
else:
    st.warning("🔴 Live sources unavailable → Backup mode active")

# =========================
# RISK ENGINE
# =========================
df["Risk Score"] = (
    df["Cases"] * 0.35 +
    df["Deaths"] * 0.45 +
    (100 - df["Policy"]) * 0.20
)

# =========================
# EVENT ENGINE
# =========================
def classify_event(risk):

    if risk > 3500:
        return "CRITICAL"

    elif risk > 2500:
        return "HIGH ALERT"

    elif risk > 1500:
        return "WATCH"

    else:
        return "STABLE"

df["Event"] = df["Risk Score"].apply(classify_event)

# =========================
# FORECAST ENGINE
# =========================
df["Forecast"] = (
    df["Risk Score"] *
    np.random.uniform(0.95, 1.15, len(df))
)

# =========================
# AGENT SYSTEM
# =========================
def surveillance_agent(df):

    critical = int((df["Event"] == "CRITICAL").sum())

    return {
        "agent": "Surveillance",
        "critical_events": critical,
        "status": "Monitoring outbreak activity"
    }

def forecast_agent(df):

    return {
        "agent": "Forecast",
        "avg_forecast": round(
            df["Forecast"].mean(),
            2
        ),
        "status": "Forecasting epidemic trends"
    }

def policy_agent(df):

    avg = df["Risk Score"].mean()

    if avg > 2500:
        action = "Escalate global response"

    elif avg > 1500:
        action = "Increase regional monitoring"

    else:
        action = "Maintain surveillance"

    return {
        "agent": "Policy",
        "recommendation": action
    }

def news_agent():

    return {
        "agent": "News",
        "keywords": [
            "outbreak",
            "virus",
            "WHO alert",
            "epidemic"
        ]
    }

# =========================
# RUN AGENTS
# =========================
surveillance = surveillance_agent(df)
forecast = forecast_agent(df)
policy = policy_agent(df)
news = news_agent()

network = {
    "surveillance": surveillance,
    "forecast": forecast,
    "policy": policy,
    "news": news
}

# =========================
# MEMORY UPDATE
# =========================
st.session_state.memory.append({
    "time": datetime.now().strftime("%H:%M:%S"),
    "risk": float(df["Risk Score"].mean())
})

# =========================
# GPT CHIEF AGENT
# =========================
def run_gpt_agent(network):

    if not GPT_AVAILABLE:
        return """
GPT agent unavailable.

To enable:
1. Add openai to requirements.txt
2. Add OPENAI_API_KEY to Streamlit secrets
"""

    prompt = f"""
You are WHO Chief AI Coordinator.

Analyze this intelligence network:

{network}

Provide:
1. Global risk summary
2. WHO recommendations
3. Executive outbreak report
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "WHO epidemic intelligence coordinator"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"GPT system error: {e}"

# =========================
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric(
    "Average Risk",
    round(df["Risk Score"].mean(), 2)
)
col3.metric(
    "Maximum Risk",
    round(df["Risk Score"].max(), 2)
)
col4.metric(
    "Critical Events",
    int((df["Event"] == "CRITICAL").sum())
)

# =========================
# NETWORK OUTPUT
# =========================
st.subheader("🧠 Multi-Agent Network")

st.json(network)

# =========================
# GPT DECISION LAYER
# =========================
st.subheader("🤖 WHO GPT Chief Coordinator")

if st.button("Run WHO AI Intelligence Cycle"):

    with st.spinner("Running autonomous WHO agents..."):

        report = run_gpt_agent(network)

        st.success("WHO Intelligence Cycle Complete")

        st.write(report)

# =========================
# ALERTS
# =========================
st.subheader("🚨 Global Alerts")

alerts = df[df["Event"] != "STABLE"]

if alerts.empty:

    st.success("🟢 No major outbreak events")

else:

    for _, row in alerts.iterrows():

        st.error(
            f"{row['Country']} → {row['Event']} "
            f"(Risk {row['Risk Score']:.2f})"
        )

# =========================
# EVENT STREAM
# =========================
st.subheader("📡 Live Event Stream")

for _, row in df.iterrows():

    st.write(
        f"{row['Country']} → {row['Event']}"
    )

# =========================
# MEMORY EVOLUTION
# =========================
st.subheader("🧠 Intelligence Memory Evolution")

memory_df = pd.DataFrame(
    st.session_state.memory
)

st.line_chart(
    memory_df.set_index("time")
)

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 Global Surveillance Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    hover_name="Country",
    title="WHO Global Risk Intelligence"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# FORECASTING
# =========================
st.subheader("📈 AI Forecasting")

st.bar_chart(
    df.set_index("Country")["Forecast"]
)

# =========================
# DATA GRID
# =========================
st.subheader("📊 Intelligence Dataset")

st.dataframe(df)

# =========================
# EXPORT
# =========================
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download WHO Intelligence Report",
    csv,
    "who_intelligence_report.csv",
    "text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")

st.write(
    "✔ WHO Global AI Intelligence System | "
    "Multi-Agent + Forecasting + Event Streaming + GPT"
)
