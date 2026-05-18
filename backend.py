from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI(title="WHO Intelligence Backend")

# =============================
# LOAD DATA
# =============================
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)

    latest = df[df["date"] == df["date"].max()]

    latest = latest[[
        "location",
        "total_cases_per_million",
        "total_deaths_per_million",
        "stringency_index"
    ]].dropna()

    latest = latest.rename(columns={
        "location": "Country",
        "total_cases_per_million": "Cases",
        "total_deaths_per_million": "Deaths",
        "stringency_index": "Policy"
    })

    return latest

# =============================
# RISK ENGINE
# =============================
def compute_risk(df):
    df["Risk Score"] = (
        df["Cases"] * 0.4 +
        df["Deaths"] * 0.4 +
        (100 - df["Policy"]) * 0.2
    )
    return df

# =============================
# API ENDPOINT 1
# =============================
@app.get("/health-data")
def health_data():
    df = load_data()
    df = compute_risk(df)
    return df.head(20).to_dict(orient="records")

# =============================
# API ENDPOINT 2
# =============================
@app.get("/alerts")
def alerts():
    df = load_data()
    df = compute_risk(df)

    threshold = df["Risk Score"].quantile(0.85)
    alerts = df[df["Risk Score"] > threshold]

    return alerts.to_dict(orient="records")

# =============================
# API ENDPOINT 3
# =============================
@app.get("/risk-summary")
def summary():
    df = load_data()
    df = compute_risk(df)

    return {
        "countries": len(df),
        "avg_risk": float(df["Risk Score"].mean()),
        "max_risk": float(df["Risk Score"].max())
    }
