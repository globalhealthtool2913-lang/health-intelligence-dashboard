import streamlit as st
import pandas as pd
import time
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="RW-11 Live Intelligence", layout="wide")

st.title("🌍 RW-11 Live Global Health Intelligence System")
st.caption("Real-time streaming architecture simulation")

# -----------------------------
# AUTO REFRESH (SIMULATED STREAM)
# -----------------------------
st.info("🔄 System updating every cycle (simulated live feed)")

# -----------------------------
# SIDEBAR
# -----------------------------
country = st.sidebar.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

refresh_speed = st.sidebar.slider(
    "Refresh speed (seconds)",
    3, 10, 5
)

# -----------------------------
# LIVE EVENT STREAM (SIMULATED)
# -----------------------------
def generate_events():

    base_events = [
        {"event": "Cholera outbreak detected", "country": "Ethiopia"},
        {"event": "Flood impacts hospitals", "country": "Kenya"},
        {"event": "Conflict disrupts healthcare", "country": "Sudan"},
        {"event": "Malaria surge reported", "country": "Somalia"},
        {"event": "Food insecurity rising", "country": "South Sudan"}
    ]

    # simulate "live variation"
    import random

    for e in base_events:
        e["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        e["random_noise"] = random.randint(1, 100)

    return pd.DataFrame(base_events)

df = generate_events()
df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE
# -----------------------------
def score(text):

    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "pandemic", "emergency"]
    moderate = ["flood", "conflict", "malaria", "food", "health"]

    s = 0

    for w in high:
        if w in text:
            s += 2

    for w in moderate:
        if w in text:
            s += 1

    return s

df["score"] = df["event"].apply(score)

def classify(s):
    if s >= 4:
        return "HIGH"
    elif s >= 2:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(classify)

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# ALERT ENGINE
# -----------------------------
if high >= 1:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL GLOBAL HEALTH ALERT")

elif moderate >= 2:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED HEALTH RISK")

elif moderate == 1:
    alert = "WATCH"
    st.info("🔎 WATCH STATUS")

else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# LIVE FEED
# -----------------------------
st.subheader("📊 Live Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# LIVE STATUS
# -----------------------------
st.subheader("⏱️ Live System Status")

st.write(f"""
- Last Update: {datetime.now().strftime('%H:%M:%S')}
- Country: **{country}**
- Alert Level: **{alert}**
- Events Processed: {len(df)}
""")

# -----------------------------
# AUTO REFRESH LOOP
# -----------------------------
time.sleep(refresh_speed)
st.rerun()
