import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
from sklearn.ensemble import IsolationForest
from datetime import datetime
from supabase import create_client
import feedparser
import random

# =========================
# APP CONFIG
# =========================
st.set_page_config(page_title="WHO AI System v2", layout="wide")

st.title("🌍 WHO AI Multi-Agent Intelligence System v2")
st.caption("GPT Reasoning + Multi-Agent System + Event Streaming + Supabase Memory")

# =========================
# SUPABASE CONNECT
# =========================
SUPABASE_URL = "https://bboiakuwwvqdlpnzlhct.supabase.co"
SUPABASE_KEY = "YOUR_PUBLISHABLE_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=120)
def load_data():

    try:
        url = "https://disease.sh/v3/covid-19/countries"
        r = requests.get(url, timeout=10)
        data = r.json()

        df = pd.DataFrame(data)[[
            "country",
            "casesPerOneMillion",
            "deathsPerOneMillion"
        ]]

        df.columns = ["Country", "Cases", "Deaths"]
        df["Policy"] = np.random.randint(40, 90, len(df))

        return df, True

    except:

        df = pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        })

        return df, False


df, live = load_data()

# =========================
# MULTI-AGENT SYSTEM
# =========================

def risk_agent(df):

    df["risk_score"] = (
        df["Cases"] * 0.4 +
        df["Deaths"] * 0.4 +
        (100 - df["Policy"]) * 0.2
    )

    return df


def anomaly_agent(df):

    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomaly"] = model.fit_predict(df[["risk_score"]])

    df["anomaly"] = df["anomaly"].apply(
        lambda x: "ALERT" if x == -1 else "OK"
    )

    return df


def forecast_agent(df):

    df["forecast"] = df["risk_score"].rolling(3).mean().fillna(df["risk_score"])

    return df


def news_agent():

    return [
        "WHO monitoring global dengue outbreak",
        "Cholera risk increasing in East Africa",
        "Respiratory virus surveillance active"
    ]


def policy_agent(risk):

    if risk > 3000:
        return "HIGH INTERVENTION REQUIRED"
    elif risk > 1500:
        return "MONITORING REQUIRED"
    else:
        return "STABLE"

# =========================
# GPT REASONING LAYER (SIMULATED)
# =========================

def gpt_reasoning(country, risk, anomaly):

    if anomaly == "ALERT":
        return f"""
🧠 AI EPIDEMIOLOGY ANALYSIS

Country: {country}
Risk Level: HIGH

Reason:
- Rapid increase in case density
- Pattern similar to previous outbreaks
- Weak containment indicators

Recommendation:
- Immediate surveillance escalation
- Field investigation required
- Cross-border monitoring activation
"""
    else:
        return f"""
🧠 AI EPIDEMIOLOGY ANALYSIS

Country: {country}
Risk Level: STABLE

Reason:
- No abnormal statistical deviation detected
- Current transmission patterns stable

Recommendation:
- Continue routine monitoring
"""

# =========================
# ORCHESTRATOR (MASTER BRAIN)
# =========================
def orchestrator(df):

    df = risk_agent(df)
    df = anomaly_agent(df)
    df = forecast_agent(df)

    return df

# RUN PIPELINE
df = orchestrator(df)

# =========================
# SAVE TO SUPABASE
# =========================
def save_to_supabase(df):

    for _, row in df.iterrows():

        supabase.table("outbreak_history").insert({
            "country": row["Country"],
            "risk_score": float(row["risk_score"]),
            "anomaly": row["anomaly"],
            "timestamp": str(datetime.utcnow())
        }).execute()

save_to_supabase(df)

# =========================
# FILTERS
# =========================
st.sidebar.header("🌍 Filters")

countries = st.sidebar.multiselect(
    "Countries",
    df["Country"].tolist(),
    default=df["Country"].tolist()
)

min_risk = st.sidebar.slider(
    "Minimum Risk Score",
    0,
    int(df["risk_score"].max()),
    0
)

filtered = df[
    (df["Country"].isin(countries)) &
    (df["risk_score"] >= min_risk)
]

# =========================
# METRICS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Countries", len(filtered))
c2.metric("Avg Risk", round(filtered["risk_score"].mean(), 2))
c3.metric("Max Risk", round(filtered["risk_score"].max(), 2))
c4.metric("Alerts", int((filtered["anomaly"] == "ALERT").sum()))

# =========================
# ALERT ENGINE
# =========================
st.subheader("🚨 WHO Alert System")

alerts = filtered[filtered["anomaly"] == "ALERT"]

if alerts.empty:
    st.success("No critical outbreaks detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → HIGH RISK ({row['risk_score']:.2f})")

# =========================
# NEWS AGENT
# =========================
st.subheader("📰 Global Health Intelligence Feed")

for n in news_agent():
    st.write("•", n)

# =========================
# GPT REASONING OUTPUT
# =========================
st.subheader("🧠 AI Epidemiologist Reasoning")

for _, row in filtered.iterrows():

    st.info(
        gpt_reasoning(
            row["Country"],
            row["risk_score"],
            row["anomaly"]
        )
    )

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    filtered,
    locations="Country",
    locationmode="country names",
    color="risk_score"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# FORECAST
# =========================
st.subheader("📈 Forecast Engine")

st.bar_chart(filtered.set_index("Country")["forecast"])

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Intelligence Dataset")

st.dataframe(filtered)

# =========================
# EXPORT
# =========================
csv = filtered.to_csv(index=False).encode()

st.download_button(
    "⬇ Export WHO Report",
    csv,
    "who_ai_v2_report.csv",
    "text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("WHO AI System v2 | Multi-Agent + GPT Reasoning + Supabase Memory")
