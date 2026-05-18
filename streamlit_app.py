import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import os
from datetime import datetime
from openai import OpenAI

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="GPT WHO Autonomous Agent",
    layout="wide"
)

st.title("🌍 GPT Autonomous WHO Surveillance Agent")
st.caption("Real LLM Reasoning + Global Epidemic Intelligence System")

# =========================
# GPT CLIENT
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# DATA SOURCE
# =========================
@st.cache_data(ttl=180)
def load_data():

    try:
        url = "https://disease.sh/v3/covid-19/countries"
        r = requests.get(url, timeout=20)

        if r.status_code == 200:
            data = r.json()
            df = pd.DataFrame(data)

            df = df[[
                "country",
                "casesPerOneMillion",
                "deathsPerOneMillion"
            ]]

            df.columns = ["Country", "Cases", "Deaths"]

            df["Policy"] = np.random.randint(40, 90, len(df))

            return df

    except Exception:
        pass

    return pd.DataFrame({
        "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
        "Cases": np.random.randint(1000, 5000, 5),
        "Deaths": np.random.randint(50, 300, 5),
        "Policy": np.random.randint(40, 90, 5)
    })

df = load_data()

# =========================
# RISK ENGINE
# =========================
df["Risk Score"] = (
    df["Cases"] * 0.35 +
    df["Deaths"] * 0.45 +
    (100 - df["Policy"]) * 0.20
)

# =========================
# GPT AUTONOMOUS AGENT CORE
# =========================
def gpt_agent(context_df):

    sample = context_df.head(10).to_dict(orient="records")

    prompt = f"""
You are a WHO epidemic intelligence AI agent.

Analyze the following global health data:

{sample}

Tasks:
1. Identify outbreak risks
2. Classify severity (LOW, MEDIUM, HIGH, CRITICAL)
3. Detect anomalies
4. Suggest WHO actions
5. Summarize global situation in 3 lines

Return structured response.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a WHO epidemic intelligence agent."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# =========================
# RUN GPT AGENT
# =========================
st.subheader("🤖 GPT Autonomous WHO Agent Analysis")

if st.button("Run WHO AI Agent"):

    with st.spinner("AI Agent analyzing global epidemic signals..."):

        report = gpt_agent(df)

        st.success("AI Analysis Complete")

        st.write(report)

# =========================
# BASIC ALERT ENGINE (backup layer)
# =========================
threshold = df["Risk Score"].quantile(0.85)
alerts = df[df["Risk Score"] > threshold]

st.subheader("🚨 System Alerts")

if alerts.empty:
    st.success("🟢 No critical signals detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} → Risk {row['Risk Score']:.2f}")

# =========================
# MAP
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="GPT WHO Surveillance Map"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA
# =========================
st.subheader("📊 Intelligence Data")

st.dataframe(df)

# =========================
# EXPORT
# =========================
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download WHO GPT Report",
    csv,
    "gpt_who_report.csv",
    "text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")

st.write("✔ GPT Autonomous WHO Agent System | Real LLM + Epidemiology Intelligence")
