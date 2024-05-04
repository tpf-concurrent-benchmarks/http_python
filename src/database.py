from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
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
        self.__engine = create_engine(url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def session(self) -> Session:
        return self.SessionLocal()
    
    def engine(self):
        return self.__engine
            

def get_db():
    db = DataBase().session()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()