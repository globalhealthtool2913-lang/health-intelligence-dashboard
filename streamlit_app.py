
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from database import load_data

st.set_page_config(page_title="Production Health Intelligence", layout="wide")

st.title("🌍 Production Global Health Intelligence System")

# -----------------------------
# LOAD FROM DATABASE ONLY
# -----------------------------
df = load_data()

if df.empty:
    st.warning("⚠️ No stored data yet. Run ingestion script first.")
    st.stop()

# -----------------------------
# CLEAN DATA
# -----------------------------
df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
df = df.dropna()

# -----------------------------
# ML MODEL
# -----------------------------
model = IsolationForest(contamination=0.2, random_state=42)
df["anomaly"] = model.fit_predict(df[["signal"]])

df["status"] = df["anomaly"].apply(
    lambda x: "🚨 ALERT" if x == -1 else "🟢 SAFE"
)

# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📊 Intelligence Overview")

col1, col2 = st.columns(2)
col1.metric("Signals", len(df))
col2.metric("Alerts", (df["anomaly"] == -1).sum())

st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

st.subheader("📈 Trend")
if df["signal"].mean() > df["signal"].median():
    st.error("🚨 Increasing activity detected")
else:
    st.success("🟢 Stable activity")

st.caption("Production-grade intelligence system (database-driven)")
