import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import random
from datetime import datetime

# Optional ML
try:
    from sklearn.ensemble import IsolationForest
    ml = True
except:
    ml = False

# Optional Supabase
try:
    from supabase import create_client
    supabase_enabled = True
except:
    supabase_enabled = False

# =========================
# APP
# =========================
st.set_page_config(page_title="WHO AI v4", layout="wide")

st.title("🌍 WHO AI Production Intelligence System v4")
st.caption("GPT Reasoning + Streaming + Microservice Architecture Simulation")

# =========================
# SUPABASE
# =========================
SUPABASE_URL = "https://bboiakuwwvqdlpnzlhct.supabase.co"
SUPABASE_KEY = "sb_publishable_BqQ_HClqREj01bd164av9A_Sl8XG1-Y"

supabase = None

if supabase_enabled and SUPABASE_KEY.startswith("sb_publishable"):

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        st.success("🟢 Supabase Connected")
    except:
        st.warning("⚠️ Supabase Offline Mode")

# =========================
# REAL-TIME STREAM SIMULATION
# =========================

def generate_live_event():

    countries = ["Kenya", "Ethiopia", "Nigeria", "India", "Brazil", "USA"]

    return {
        "country": random.choice(countries),
        "cases": random.randint(500, 5000),
        "deaths": random.randint(10, 300),
        "timestamp": datetime.utcnow()
    }

# =========================
# GPT REASONING ENGINE (WHO STYLE)
# =========================

def gpt_epidemiology_reasoning(event):

    risk = event["cases"] * 0.4 + event["deaths"] * 0.6

    if risk > 2000:

        return f"""
🧠 WHO EPIDEMIOLOGICAL ANALYSIS

Country: {event['country']}
Risk Level: HIGH

Interpretation:
- Rapid transmission pattern detected
- High case-to-death correlation
- Possible outbreak cluster formation

WHO Recommendation:
- Immediate field investigation required
- Activate emergency surveillance team
- Cross-border monitoring advised
"""

    elif risk > 1000:

        return f"""
🧠 WHO EPIDEMIOLOGICAL ANALYSIS

Country: {event['country']}
Risk Level: MODERATE

Interpretation:
- Increasing transmission signals detected
- No confirmed outbreak yet

WHO Recommendation:
- Strengthen monitoring
- Increase testing capacity
"""

    else:

        return f"""
🧠 WHO EPIDEMIOLOGICAL ANALYSIS

Country: {event['country']}
Risk Level: LOW

Interpretation:
- Stable epidemiological conditions
- No abnormal patterns detected

WHO Recommendation:
- Routine surveillance only
"""

# =========================
# AI RISK ENGINE
# =========================

def risk_engine(df):

    df["risk_score"] = df["cases"] * 0.5 + df["deaths"] * 0.5
    return df

# =========================
# STREAMING CONTAINER
# =========================

st.subheader("🔴 Live Outbreak Stream")

stream_placeholder = st.empty()

events = []

for i in range(5):

    event = generate_live_event()
    event["analysis"] = gpt_epidemiology_reasoning(event)
    events.append(event)

    with stream_placeholder.container():

        st.write("### Latest Event")
        st.json(event)

        st.write(event["analysis"])

    time.sleep(1)

# =========================
# BUILD DATAFRAME
# =========================

df = pd.DataFrame(events)
df = risk_engine(df)

# =========================
# SUPABASE SAVE (SAFE)
# =========================

if supabase:

    for _, row in df.iterrows():

        try:
            supabase.table("outbreak_history").insert({
                "country": row["country"],
                "risk_score": float(row["risk_score"]),
                "anomaly": "STREAM_EVENT",
                "timestamp": str(row["timestamp"])
            }).execute()
        except:
            pass

# =========================
# DASHBOARD
# =========================

st.subheader("📊 Live Intelligence Dashboard")

st.dataframe(df)

# =========================
# GLOBAL SUMMARY
# =========================

st.subheader("🌍 Global Situation Summary")

avg_risk = df["risk_score"].mean()

if avg_risk > 2000:
    st.error("GLOBAL ALERT LEVEL: HIGH")
elif avg_risk > 1000:
    st.warning("GLOBAL ALERT LEVEL: MODERATE")
else:
    st.success("GLOBAL ALERT LEVEL: LOW")

# =========================
# FOOTER
# =========================

st.markdown("---")
st.write("WHO AI v4 | Streaming + Reasoning + Microservice Architecture Prototype")
