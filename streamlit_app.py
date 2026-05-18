import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="WHO Streaming System", layout="wide")

st.title("🌍 WHO Real-Time Streaming Intelligence System")

# =========================
# CALL BACKEND STREAM
# =========================
@st.cache_data(ttl=60)
def get_stream():

    try:
        r = requests.get("http://localhost:8000/stream", timeout=10)
        data = r.json()

        df = pd.DataFrame(data["data"])

        df = df.rename(columns={
            "location": "Country",
            "total_cases_per_million": "Cases",
            "total_deaths_per_million": "Deaths",
            "stringency_index": "Policy"
        })

        return df

    except Exception:
        return None

df = get_stream()

if df is None:
    st.error("Backend not running (FastAPI)")
    st.stop()

# =========================
# AI RISK ENGINE
# =========================
df["Risk"] = df["Cases"] * 0.3 + df["Deaths"] * 0.4 + (100 - df["Policy"]) * 0.3

# =========================
# ALERT SYSTEM
# =========================
threshold = df["Risk"].quantile(0.85)

st.subheader("🚨 Live Alerts")

alerts = df[df["Risk"] > threshold]

for _, row in alerts.iterrows():
    st.error(f"{row['Country']} → Risk {row['Risk']:.2f}")

# =========================
# MAP
# =========================
st.subheader("🌍 Live Global Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE
# =========================
st.subheader("📊 Live Data")

st.dataframe(df)
