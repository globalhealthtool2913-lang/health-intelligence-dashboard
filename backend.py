from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

# =========================
# HEALTH RISK SERVICE
# =========================
@app.get("/risk")
def risk():

    countries = ["Kenya", "USA", "India", "Brazil", "Ethiopia"]

    return {
        "timestamp": str(datetime.utcnow()),
        "data": [
            {
                "country": c,
                "risk": random.randint(1000, 5000)
            }
            for c in countries
        ]
    }

# =========================
# OUTBREAK NEWS SERVICE
# =========================
@app.get("/news")
def news():

    return {
        "alerts": [
            "WHO monitoring dengue outbreak",
            "Cholera risk increasing in East Africa",
            "Respiratory virus surveillance active"
        ]
    }
