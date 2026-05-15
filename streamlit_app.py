import streamlit as st
import pandas as pd
import time
import random

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence RW-6", layout="wide")

st.title("🌍 Global Health Intelligence System (RW-6 LIVE)")
st.caption("Live-stream simulation (auto-refresh intelligence feed)")

# -----------------------------
# COUNTRY
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# SIMULATED LIVE DATA ENGINE
# -----------------------------
def get_live_data():
    base_data = [
        {"event": "Cholera outbreak suspected in flood region", "country": "Ethiopia"},
        {"event": "Measles cases increasing in camps", "country": "Sudan"},
        {"event": "Flooding disrupting clinics", "country": "Kenya"},
        {"event": "Malaria surge in rural districts", "country": "Somalia"},
        {"event": "Food insecurity affecting children", "country": "South Sudan"},
    ]

    # simulate "live changes"
    random.shuffle(base_data)
    return pd.DataFrame(base_data)

# -----------------------------
# RISK ENGINE
# -----------------------------
def score(text):
    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "surge"]
    moderate = ["conflict", "flood", "malaria", "food", "displacement"]

    s = 0
    for w in high:
        if w in text:
            s += 2
    for w in moderate:
        if w in text:
            s += 1

    return s

def classify(s):
    if s >= 3:
        return "HIGH"
    elif s == 2:
        return "MODERATE"
    return "LOW"

# -----------------------------
# LIVE STREAM PLACEHOLDER
# -----------------------------
placeholder = st.empty()

# -----------------------------
# LIVE LOOP (SAFE SIMULATION)
# -----------------------------
for i in range(3):

    df = get_live_data()
    df = df[df["country"] == country]

    df["score"] = df["event"].apply(score)
    df["risk"] = df["score"].apply(classify)

    high = int((df["risk"] == "HIGH").sum())
    moderate = int((df["risk"] == "MODERATE").sum())
    low = int((df["risk"] == "LOW").sum())

    with placeholder.container():

        st.subheader("🔴 LIVE INTELLIGENCE STREAM")

        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 High", high)
        col2.metric("🟠 Moderate", moderate)
        col3.metric("🟢 Low", low)

        st.subheader("📊 Intelligence Feed")
        st.dataframe(df, use_container_width=True)

        # ALERT
        if high >= 1:
            st.error("🚨 CRITICAL RISK DETECTED")
        elif moderate >= 1:
            st.warning("⚠️ ELEVATED RISK DETECTED")
        else:
            st.success("🟢 STABLE CONDITIONS")

        st.write(f"⏱️ Live update cycle: {i+1}/3")

    time.sleep(3)

# -----------------------------
# FINAL REPORT
# -----------------------------
st.divider()
st.subheader("🧠 Final Situation Report")

st.write("""
This system simulates real-time outbreak intelligence updates.
Used for monitoring evolving health risks across regions.
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-6 LIVE - Simulated Real-Time Global Health Intelligence System")
