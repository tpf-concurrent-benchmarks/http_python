from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.controllers import users, polls, votes, sessions

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(polls.router)
app.include_router(votes.router)