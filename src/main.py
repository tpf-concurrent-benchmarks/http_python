from fastapi import FastAPI
from src.endpoints import users, polls, votes

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(polls.router)
app.include_router(votes.router)