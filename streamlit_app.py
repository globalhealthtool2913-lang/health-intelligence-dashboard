import streamlit as st
import pandas as pd
from datetime import datetime
import random

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="RW-12 Global Health Intelligence",
    layout="wide"
)

st.title("🌍 RW-12 Global Health Intelligence Platform")
st.caption("Architecture-level surveillance system (pipeline-based design)")

# -----------------------------
# SIDEBAR
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.sidebar.markdown("### Filters")
show_high = st.sidebar.checkbox("High Risk", True)
show_mod = st.sidebar.checkbox("Moderate Risk", True)
show_low = st.sidebar.checkbox("Low Risk", True)

# -----------------------------
# SIMULATED DATA PIPELINE (RW-12 STYLE)
# -----------------------------
def ingest_data():

    base = [
        {"event": "Cholera outbreak reported", "country": "Ethiopia", "source": "WHO"},
        {"event": "Flood affecting hospitals", "country": "Kenya", "source": "ReliefWeb"},
        {"event": "Conflict limiting healthcare access", "country": "Sudan", "source": "UNICEF"},
        {"event": "Malaria surge detected", "country": "Somalia", "source": "Africa CDC"},
        {"event": "Food insecurity worsening", "country": "South Sudan", "source": "WHO"}
    ]

    # simulate dynamic updates
    for b in base:
        b["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        b["noise"] = random.randint(1, 100)

    return pd.DataFrame(base)

df = ingest_data()

df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE (WEIGHTED RW-12 VERSION)
# -----------------------------
def risk_score(text):

    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "pandemic", "emergency"]
    moderate = ["flood", "conflict", "malaria", "food", "health"]

    score = 0

    for w in high:
        if w in text:
            score += 3  # weighted higher

    for w in moderate:
        if w in text:
            score += 1

    return score

df["score"] = df["event"].apply(risk_score)

# -----------------------------
# CLASSIFICATION ENGINE
# -----------------------------
def classify(s):

    if s >= 6:
        return "HIGH"
    elif s >= 3:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(classify)

# -----------------------------
# FILTERING
# -----------------------------
allowed = []
if show_high:
    allowed.append("HIGH")
if show_mod:
    allowed.append("MODERATE")
if show_low:
    allowed.append("LOW")

df = df[df["risk"].isin(allowed)]

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

c1, c2, c3 = st.columns(3)
c1.metric("🔴 High", high)
c2.metric("🟠 Moderate", moderate)
c3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT ENGINE (RW-12 REALISTIC)
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
st.dataframe(df, use_container_width=True)

# -----------------------------
# PIPELINE VISUALIZATION (SIMPLE RW-12 MODEL)
# -----------------------------
st.subheader("⚙️ Processing Pipeline")

st.code("""
DATA INGESTION → CLEANING → RISK SCORING → CLASSIFICATION → ALERT ENGINE → DASHBOARD
""")

# -----------------------------
# TREND ANALYSIS
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend = "STABLE"

if trend_score >= 8:
    trend = "RISING FAST 📈"
elif trend_score >= 5:
    trend = "MODERATE RISK ⚠️"
elif trend_score >= 2:
    trend = "LOW ACTIVITY 📉"

st.write(f"Trend Status: **{trend}**")

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

st.write(f"""
### RW-12 Intelligence Summary

- Country: **{country}**
- Alert Level: **{alert}**
- Trend Status: **{trend}**

### Metrics
- High: {high}
- Moderate: {moderate}
- Low: {low}

### Interpretation
This reflects a **{alert.lower()}-level operational intelligence environment**.

### Recommendation
{"Activate emergency coordination immediately." if alert=="CRITICAL"
else "Increase surveillance operations." if alert=="ELEVATED"
else "Maintain monitoring systems."}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-12 - Architecture-Level Global Health Intelligence System")
