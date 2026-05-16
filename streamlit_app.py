import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Global Health Intelligence System", layout="wide")

st.title("🌍 Global Health Intelligence System (Always Live Mode)")
st.caption("Never-blank dashboard with resilient multi-source intelligence")

# -----------------------------
# SOURCE 1: GDELT
# -----------------------------
def get_gdelt():
    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "health OR outbreak OR epidemic OR virus OR disease",
            "mode": "ArtList",
            "format": "json"
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        articles = data.get("articles", [])

        return pd.DataFrame([{
            "source": "GDELT",
            "country": a.get("sourceCountry", "Unknown"),
            "signal": 1
        } for a in articles])

    except:
        return pd.DataFrame()

# -----------------------------
# SOURCE 2: OWID
# -----------------------------
def get_owid():
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url, low_memory=False)

        df = df[["location", "total_cases"]].dropna()
        df = df.rename(columns={
            "location": "country",
            "total_cases": "signal"
        })

        df["source"] = "OWID"

        return df.groupby("country").tail(1)

    except:
        return pd.DataFrame()

# -----------------------------
# LOAD DATA (NO FAIL STOP)
# -----------------------------
gdelt = get_gdelt()
owid = get_owid()

frames = []

if not gdelt.empty:
    frames.append(gdelt)

if not owid.empty:
    frames.append(owid)

# -----------------------------
# ALWAYS SHOW DASHBOARD (IMPORTANT FIX)
# -----------------------------
if len(frames) == 0:
