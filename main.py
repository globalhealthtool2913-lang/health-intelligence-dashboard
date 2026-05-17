from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "WORKING"}

@app.get("/health")
def health():
    return {"ok": True}
