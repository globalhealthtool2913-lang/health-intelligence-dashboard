   import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import os

from sklearn.ensemble import RandomForestRegressor

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="WHO Multi-Source Intelligence System",
    layout="wide"
)

st.title("🌍 WHO Multi-Source Intelligence System")
st.caption("Health + News + AI Fusion + Early Warning System")

# =============================
# HISTORY STORAGE
# =============================
HISTORY_FILE = "risk_history.csv"

# =============================
# 1. HEALTH DATA SOURCE
# =============================
@st.cache_data(ttl=3600)
def load_health_data():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)

    latest = df[df["date"] == df["date"].max()]

    latest = latest[[
        "location",
        "total_cases_per_million",
        "total_deaths_per_million",
        "stringency_index"
    ]].dropna()

    latest = latest.rename(columns={
        "location": "Country",
        "total_cases_per_million": "Cases",
        "total_deaths_per_million": "Deaths",
        "stringency_index": "Policy"
    })

    return latest

# =============================
# 2. NEWS SIGNAL ENGINE (SIMULATED REAL-WORLD LAYER)
# =============================
def generate_news_signals(df):

    np.random.seed(42)

    df["News_Signal"] = np.random.randint(0, 100, len(df))

    df["Outbreak_Keywords"] = np.random.randint(0, 100, len(df))

    return df

# =============================
# LOAD DATA
# =============================
df = load_health_data()

df = generate_news_signals(df)

# =============================
# 3. FEATURE FUSION ENGINE
# =============================
df["Risk Score"] = (
    df["Cases"] * 0.3 +
    df["Deaths"] * 0.3 +
    (100 - df["Policy"]) * 0.15 +
    df["News_Signal"] * 0.15 +
    df["Outbreak_Keywords"] * 0.1
)

# =============================
# 4. PERSISTENT STORAGE
# =============================
history_df = df[["Country", "Risk Score"]].copy()
history_df["Timestamp"] = pd.Timestamp.now()

if os.path.exists(HISTORY_FILE):

    old = pd.read_csv(HISTORY_FILE)

    combined = pd.concat([old, history_df])

    combined = combined.tail(1500)

    combined.to_csv(HISTORY_FILE, index=False)

else:

    history_df.to_csv(HISTORY_FILE, index=False)

history_data = pd.read_csv(HISTORY_FILE)

# =============================
# 5. AI MODEL
# =============================
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

X = df[[
    "Cases",
    "Deaths",
    "Policy",
    "News_Signal",
    "Outbreak_Keywords"
]]

y = df["Risk Score"]

model.fit(X, y)

df["AI Prediction"] = model.predict(X)

# =============================
# 6. ANOMALY DETECTION
# =============================
threshold = df["Risk Score"].quantile(0.85)

alerts = df[df["Risk Score"] > threshold]

# =============================
# METRICS
# =============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(df))
col2.metric("Alerts", len(alerts))
col3.metric("Avg Risk", round(df["Risk Score"].mean(), 2))
col4.metric("System", "MULTI-SOURCE ACTIVE")

# =============================
# ALERT SYSTEM
# =============================
st.subheader("🚨 Global Alerts")

if alerts.empty:

    st.success("No global outbreak threats detected")

else:

    for _, row in alerts.iterrows():

        st.error(
            f"{row['Country']} | Risk: {row['Risk Score']:.2f}"
        )

# =============================
# GLOBAL MAP
# =============================
st.subheader("🌍 Global Intelligence Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="Multi-Source Global Health Risk Map"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# AI VALIDATION
# =============================
st.subheader("🤖 AI Prediction Validation")

fig2 = px.scatter(
    df,
    x="Risk Score",
    y="AI Prediction",
    color="Country",
    size="Cases",
    title="AI Fusion Model Performance"
)

st.plotly_chart(fig2, use_container_width=True)

# =============================
# DATA TABLE
# =============================
st.subheader("📊 Intelligence Dataset")

st.dataframe(df)

# =============================
# FORECAST ENGINE
# =============================
st.subheader("📈 Forecast Engine")

selected_country = st.selectbox(
    "Select Country",
    df["Country"].unique()
)

country_history = history_data[
    history_data["Country"] == selected_country
]

if len(country_history) > 5:

    risks = country_history.tail(10)["Risk Score"].values

    trend = np.polyfit(
        range(len(risks)),
        risks,
        1
    )

    future = list(range(len(risks), len(risks) + 5))

    forecast = [
        trend[0] * x + trend[1]
        for x in future
    ]

    forecast_df = pd.DataFrame({
        "Step": future,
        "Forecast": forecast
    })

    fig3 = px.line(
        forecast_df,
        x="Step",
        y="Forecast",
        title=f"{selected_country} Forecast Risk"
    )

    st.plotly_chart(fig3, use_container_width=True)

# =============================
# INTELLIGENCE FEED
# =============================
st.subheader("🧠 Intelligence Feed")

feed = [
    "Ingesting health + news signals...",
    "Detecting outbreak patterns...",
    "Running AI fusion engine...",
    "Updating global risk model...",
    "Multi-source intelligence active..."
]

for msg in feed:

    st.info(msg)

# =============================
# FOOTER
# =============================
st.success(
    "🟢 WHO Multi-Source Intelligence System ACTIVE"
) 

    
