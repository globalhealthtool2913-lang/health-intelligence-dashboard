import streamlit as st
import pandas as pd
from datetime import datetime
import random

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-13 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-13 Global Health Intelligence System")
st.caption("Advanced intelligence architecture with trend memory + scoring engine")

# -----------------------------
# SESSION MEMORY (SIMULATED DATABASE)
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# SIDEBAR
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.sidebar.markdown("### Controls")
run_cycle = st.sidebar.button("🔄 Run Intelligence Cycle")

# -----------------------------
# SIMULATED DATA INGESTION LAYER
# -----------------------------
def ingest_data():

    base_events = [
        {"event": "Cholera outbreak reported", "country": "Ethiopia", "source": "WHO"},
        {"event": "Flooding affecting hospitals", "country": "Kenya", "source": "ReliefWeb"},
        {"event": "Conflict limiting healthcare access", "country": "Sudan", "source": "UNICEF"},
        {"event": "Malaria surge detected", "country": "Somalia", "source": "Africa CDC"},
        {"event": "Food insecurity worsening", "country": "South Sudan", "source": "WHO"}
    ]

    for e in base_events:
        e["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        e["noise"] = random.randint(1, 100)

    return pd.DataFrame(base_events)

# -----------------------------
# RISK ENGINE (WEIGHTED RW-13)
# -----------------------------
def risk_score(text):

    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "pandemic", "emergency"]
    moderate = ["flood", "conflict", "malaria", "food", "health"]

    score = 0

    for w in high:
        if w in text:
            score += 3

    for w in moderate:
        if w in text:
            score += 1

    return score

def classify(score):

    if score >= 6:
        return "HIGH"
    elif score >= 3:
        return "MODERATE"
    return "LOW"

# -----------------------------
# RUN INTELLIGENCE CYCLE
# -----------------------------
if run_cycle:

    df = ingest_data()
    df = df[df["country"] == country]

    df["score"] = df["event"].apply(risk_score)
    df["risk"] = df["score"].apply(classify)

    # store in "memory"
    st.session_state.history.append(df)

# -----------------------------
# DISPLAY HISTORY (SIMULATED DATABASE)
# -----------------------------
st.subheader("🗄️ Intelligence History (Session Memory)")

if st.session_state.history:
    history_df = pd.concat(st.session_state.history)
    history_df = history_df[history_df["country"] == country]

    st.dataframe(history_df, use_container_width=True)

    high = int((history_df["risk"] == "HIGH").sum())
    moderate = int((history_df["risk"] == "MODERATE").sum())
    low = int((history_df["risk"] == "LOW").sum())

else:
    st.info("Run an intelligence cycle to generate data.")

    high, moderate, low = 0, 0, 0

# -----------------------------
# METRICS
# -----------------------------
c1, c2, c3 = st.columns(3)
c1.metric("🔴 High", high)
c2.metric("🟠 Moderate", moderate)
c3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# TREND ENGINE (CORE RW-13 FEATURE)
# -----------------------------
trend_score = (high * 3) + moderate

if "trend_history" not in st.session_state:
    st.session_state.trend_history = []

st.session_state.trend_history.append(trend_score)

if len(st.session_state.trend_history) > 1:
    if st.session_state.trend_history[-1] > st.session_state.trend_history[-2]:
        trend = "RISING 📈"
    elif st.session_state.trend_history[-1] < st.session_state.trend_history[-2]:
        trend = "DECLINING 📉"
    else:
        trend = "STABLE ➖"
else:
    trend = "INITIALIZING"

# -----------------------------
# ALERT ENGINE (REALISTIC RW-13)
# -----------------------------
if trend_score > 8 and trend == "RISING 📈":
    alert = "CRITICAL"
elif trend_score > 5:
    alert = "ELEVATED"
elif trend_score > 2:
    alert = "WATCH"
else:
    alert = "STABLE"

# -----------------------------
# SUMMARY DASHBOARD
# -----------------------------
st.subheader("📊 Intelligence Summary")

st.write(f"""
- Country: **{country}**
- Alert Level: **{alert}**
- Trend Status: **{trend}**
- Trend Score: **{trend_score}**
""")

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

st.write(f"""
### RW-13 Intelligence Output

This system is monitoring **{country}** using a multi-cycle intelligence engine.

### Key Findings
- High-risk signals: {high}
- Moderate-risk signals: {moderate}
- Low-risk signals: {low}

### Interpretation
The system indicates a **{alert.lower()}-level operational environment**.

### Recommendation
{"Activate emergency response protocols." if alert=="CRITICAL"
else "Increase surveillance intensity." if alert=="ELEVATED"
else "Maintain routine monitoring operations."}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-13 - Intelligence System with Memory + Trend Evolution")
