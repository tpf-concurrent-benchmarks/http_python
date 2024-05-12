from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
import os

class DataBaseMeta(type):
    __instance: "DataBase" = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            instance = super().__call__(*args, **kwargs)
            cls.__instance = instance
        return cls.__instance

class DataBase(metaclass=DataBaseMeta):
    def __init__(self):
        url = os.getenv("DATABASE_URL")
        self.__engine = create_async_engine(url, pool_size=50, max_overflow=-1)
        self.SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def session(self) -> AsyncSession:
        return self.SessionLocal()
    
    def engine(self) -> AsyncEngine:
        return self.__engine
            

async def get_db():
    async with DataBase().session() as db:
        try:
            yield db
            await db.commit()
        except:
            await db.rollback()
            raise
        finally:
            await db.close()