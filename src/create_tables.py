from dotenv import load_dotenv
load_dotenv()

from src.database import DataBase
from src.models import Base

def main():
    Base.metadata.create_all(DataBase().engine())

if __name__ == "__main__":
    main()