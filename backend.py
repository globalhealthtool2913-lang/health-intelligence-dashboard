from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="WHO AI Core Engine")

class CountryData(BaseModel):
    country: str
    cases: float
    deaths: float
    policy: float

# =========================
# RISK ENGINE
# =========================
@app.post("/risk")
def compute_risk(data: CountryData):

    risk = (
        data.cases * 0.4 +
        data.deaths * 0.4 +
        (100 - data.policy) * 0.2
    )

    return {
        "country": data.country,
        "risk": risk
    }

# =========================
# ANOMALY DETECTION (SIMPLE VERSION)
# =========================
@app.post("/anomaly")
def detect_anomaly(values: list[float]):

    mean = np.mean(values)
    std = np.std(values)

    anomalies = [
        v for v in values
        if abs(v - mean) > 2 * std
    ]

    return {
        "anomalies": anomalies
    }

# =========================
# FORECAST ENGINE
# =========================
@app.post("/forecast")
def forecast(values: list[float]):

    trend = np.mean(values[-5:]) * 1.1

    return {
        "forecast": trend
    }
