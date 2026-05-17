from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "WHO backend running"}

@app.get("/alerts")
def alerts():
    return {
        "alerts": [
            {
                "country": "Ethiopia",
                "risk": 65,
                "level": "TEST ALERT"
            }
        ]
    }
