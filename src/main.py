from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.controllers import users, polls, votes, sessions
from src.database import DataBase
from src.models import Base

async def lifespan(app: FastAPI):
    db = DataBase()
    Base.metadata.create_all(bind=db.engine())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
    
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(polls.router)
app.include_router(votes.router)