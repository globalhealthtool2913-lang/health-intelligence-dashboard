import streamlit as st
import pandas as pd
from datetime import datetime
import random

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-14 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-14 Global Health Intelligence Platform")
st.caption("Production-style intelligence frontend (pipeline-connected design)")

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

run = st.sidebar.button("🔄 Run Intelligence Cycle")

# -----------------------------
# SIMULATED INTELLIGENCE INPUT (API LAYER MOCK)
# -----------------------------
def fetch_events():

    return [
        {
            "event": "Cholera outbreak detected",
            "country": "Ethiopia",
            "source": "WHO",
        },
        {
            "event": "Flooding affecting hospitals",
            "country": "Kenya",
            "source": "ReliefWeb",
        },
        {
            "event": "Conflict limiting healthcare access",
            "country": "Sudan",
            "source": "UNICEF",
        },
        {
            "event": "Malaria surge reported",
            "country": "Somalia",
            "source": "Africa CDC",
        },
        {
            "event": "Food insecurity worsening",
            "country": "South Sudan",
            "source": "WHO",
        }
    ]

# -----------------------------
# RISK ENGINE (WEIGHTED RW-14)
# -----------------------------
def score(text):

    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "pandemic", "emergency"]
    moderate = ["flood", "conflict", "malaria", "food", "health"]

    s = 0

    for w in high:
        if w in text:
            s += 3

    for w in moderate:
        if w in text:
            s += 1

    return s

def classify(s):
    if s >= 6:
        return "HIGH"
    elif s >= 3:
        return "MODERATE"
    return "LOW"

# -----------------------------
# SESSION STATE (SIMULATED DATABASE)
# -----------------------------
if "db" not in st.session_state:
    st.session_state.db = []

# -----------------------------
# RUN PIPELINE
# -----------------------------
if run:

    raw = fetch_events()

    df = pd.DataFrame(raw)

    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["noise"] = [random.randint(1, 100) for _ in range(len(df))]

    df = df[df["country"] == country]

    df["score"] = df["event"].apply(score)
    df["risk"] = df["score"].apply(classify)

    st.session_state.db.append(df)

# -----------------------------
# LOAD DATA
# -----------------------------
if st.session_state.db:
    data = pd.concat(st.session_state.db)
    data = data[data["country"] == country]
else:
    data = pd.DataFrame(columns=["event","country","source","timestamp","score","risk"])

# -----------------------------
# METRICS
# -----------------------------
high = (data["risk"] == "HIGH").sum()
moderate = (data["risk"] == "MODERATE").sum()
low = (data["risk"] == "LOW").sum()

c1, c2, c3 = st.columns(3)
c1.metric("🔴 High", high)
c2.metric("🟠 Moderate", moderate)
c3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT ENGINE
# -----------------------------
trend_score = (high * 3) + moderate

if trend_score >= 8:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

elif trend_score >= 5:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")

elif trend_score >= 2:
    alert = "WATCH"
    st.info("🔎 WATCH STATUS")

else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# INTELLIGENCE FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(data, use_container_width=True)

# -----------------------------
# PIPELINE VIEW
# -----------------------------
st.subheader("⚙️ System Pipeline")

st.code("""
INGESTION → NORMALIZATION → SCORING → CLASSIFICATION → ALERT ENGINE → DASHBOARD
""")

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

st.write(f"""
### RW-14 Intelligence Summary

- Country: **{country}**
- Alert Level: **{alert}**
- Trend Score: **{trend_score}**

### Interpretation
This represents a **{alert.lower()} operational intelligence state**.

### Recommendation
{"Activate emergency response immediately." if alert=="CRITICAL"
else "Increase monitoring intensity." if alert=="ELEVATED"
else "Maintain routine surveillance."}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-14 - Production-Style Global Health Intelligence Frontend")
    
