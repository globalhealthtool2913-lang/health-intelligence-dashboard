from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "WHO backend running"}

@app.get("/alerts")
def alerts():
    return {
        "alerts": [
            {"country": "Ethiopia", "risk": 70},
            {"country": "USA", "risk": 55}
        ]
    }

@app.get("/signals")
def signals():
    return [
        {"country": "Ethiopia", "signal": 3},
        {"country": "USA", "signal": 5}
    ]
