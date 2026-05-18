from fastapi import FastAPI
import requests
import pandas as pd
import io
import time

app = FastAPI()

CACHE = {}

# =========================
# LIVE DATA STREAM FUNCTION
# =========================
def fetch_data():

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    r = requests.get(url, timeout=20)
    df = pd.read_csv(io.StringIO(r.text))

    latest = df[df["date"] == df["date"].max()]

    latest = latest[[
        "location",
        "total_cases_per_million",
        "total_deaths_per_million",
        "stringency_index"
    ]].dropna()

    return latest.to_dict()

# =========================
# STREAM ENDPOINT
# =========================
@app.get("/stream")
def stream_data():

    global CACHE

    data = fetch_data()
    CACHE = {
        "timestamp": time.time(),
        "data": data
    }

    return CACHE
