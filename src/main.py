from fastapi import FastAPI
from src import users, polls

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(polls.router)