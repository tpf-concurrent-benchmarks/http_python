from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import sqlalchemy
import asyncio
from src.controllers import users, polls, votes, sessions
from src.database import DataBase
from src.models import Base

async def lifespan(app: FastAPI):
    db = DataBase()
    retries = 5
    for i in range(retries):
        try:
            Base.metadata.create_all(bind=db.engine())
            break
        except sqlalchemy.exc.OperationalError as e:
            if i == retries - 1:
                raise e
            await asyncio.sleep(2)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
    
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(polls.router)
app.include_router(votes.router)