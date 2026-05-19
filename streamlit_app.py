import streamlit as st
import requests
import pandas as pd
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="WHO AI Dashboard", layout="wide")

st.title("🌍 WHO AI Intelligence Dashboard")
st.caption("Frontend connected to FastAPI backend")

# 👉 CHANGE THIS AFTER DEPLOYING FASTAPI
API_BASE = "https://your-fastapi-app.onrender.com"

# =========================
# FUNCTIONS
# =========================

def get_events():
    try:
        r = requests.get(f"{API_BASE}/events", timeout=10)
        return r.json()
    except:
        return []

def get_latest():
    try:
        r = requests.get(f"{API_BASE}/latest", timeout=10)
        return r.json()
    except:
        return None

# =========================
# LIVE DASHBOARD
# =========================

st.subheader("🔴 Live Outbreak Stream")

placeholder = st.empty()

events = get_events()

if events:

    df = pd.DataFrame(events)

    with placeholder.container():

        st.write("### Recent Events")
        st.dataframe(df)

        st.write("### Latest Event")

        latest = get_latest()
        if latest:
            st.json(latest)

else:
    st.warning("No data from backend. Check FastAPI deployment.")

# =========================
# REFRESH LOOP (SIMULATED LIVE)
# =========================

st.subheader("🔄 Auto Refresh View")

if st.button("Refresh Now"):
    st.rerun()

st.write("Auto-updating every 5 seconds...")

time.sleep(5)
st.rerun()
