from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "SERVER IS RUNNING"}

@app.get("/test")
def test():
    return {"message": "OK"}
