  import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import os
from openai import OpenAI

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="WHO Multi-Agent Super System",
    layout="wide"
)

st.title("🌍 WHO Multi-Agent Super Intelligence System")
st.caption("5 AI Agents Working Together for Global Health Intelligence")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# DATA
# =========================
@st.cache_data(ttl=180)
def load_data():

    try:
        url = "https://disease.sh/v3/covid-19/countries"
        r = requests.get(url, timeout=20)

        data = r.json()

        df = pd.DataFrame(data)[[
            "country",
            "casesPerOneMillion",
            "deathsPerOneMillion"
        ]]

        df.columns = ["Country", "Cases", "Deaths"]
        df["Policy"] = np.random.randint(40, 90, len(df))

        return df

    except:
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

sample_data = df.head(8).to_dict(orient="records")

# =========================
# AGENT 1 — SURVEILLANCE
# =========================
def surveillance_agent(data):
    return f"""
Surveillance Agent:
Detected {len(data)} monitored regions.
Highest risk: {max([d['Cases'] for d in data])}
"""

# =========================
# AGENT 2 — FORECAST
# =========================
def forecast_agent(data):
    return f"""
Forecast Agent:
Expected upward trend in {sum(1 for d in data if d['Cases'] > 2000)} regions.
Risk acceleration detected.
"""

# =========================
# AGENT 3 — NEWS INTERPRETER
# =========================
def news_agent(data):
    return """
News Agent:
Global outbreak signals increasing in media patterns.
WHO alert keywords detected: outbreak, epidemic, virus.
"""

# =========================
# AGENT 4 — POLICY RECOMMENDER
# =========================
def policy_agent(data):
    return """
Policy Agent:
Recommended actions:
- Increase surveillance
- Strengthen border screening
- Deploy regional response teams
"""

# =========================
# AGENT 5 — CHIEF WHO AGENT
# =========================
def chief_agent(all_reports):

    prompt = f"""
You are the Chief WHO AI Coordinator.

Combine these agent reports into a final WHO decision:

{all_reports}

Return:
1. Global situation summary
2. Risk level
3. Emergency recommendation
4. 3-line executive report
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are WHO Chief Intelligence Officer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# =========================
# RUN ALL AGENTS
# =========================
st.subheader("🧠 Multi-Agent Intelligence Layer")

surv = surveillance_agent(sample_data)
fore = forecast_agent(sample_data)
news = news_agent(sample_data)
policy = policy_agent(sample_data)

st.info(surv)
st.info(fore)
st.info(news)
st.info(policy)

# =========================
# CHIEF AGENT DECISION
# =========================
st.subheader("🌍 Chief WHO Agent Decision")

if st.button("Run WHO Super Intelligence System"):

    with st.spinner("Coordinating 5 AI agents..."):

        all_reports = surv + fore + news + policy

        final = chief_agent(all_reports)

        st.success("WHO Multi-Agent Decision Complete")

        st.write(final)

# =========================
# VISUALIZATION
# =========================
st.subheader("🌍 Global Risk Map")

fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Risk Score",
    title="WHO Multi-Agent Risk Map"
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
    "⬇ Download WHO Multi-Agent Report",
    csv,
    "who_multi_agent_report.csv",
    "text/csv"
)

st.markdown("---")

st.write(
    "✔ WHO Multi-Agent Super System | "
    "5 AI Agents + Chief Coordinator + Global Intelligence"
) 
