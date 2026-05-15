from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    high: int
    moderate: int
    low: int

@app.get("/events")
def events():
    return [
        {"country": "Ethiopia", "risk": "HIGH", "score": 9},
        {"country": "Kenya", "risk": "MODERATE", "score": 5},
        {"country": "Uganda", "risk": "LOW", "score": 2}
    ]

@app.post("/predict")
def predict(data: InputData):

    score = (data.high * 4) + (data.moderate * 2) + data.low
    probability = min(score / 12, 1.0)

    return {
        "risk_score": score,
        "probability": probability
    }
