from fastapi import FastAPI
from src import users

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(users.router)