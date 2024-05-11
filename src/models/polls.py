from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm.session import Session
from typing import List, Optional

from src.models.poll_options import PollOptionModel
from src.models import Base
from src.models.users import UserModel

class PollModel(Base):
    __tablename__ = "polls"

    poll_id: Mapped[int] = mapped_column(primary_key=True)
    poll_topic: Mapped[str] = mapped_column()
    creator_id: Mapped["UserModel"] = mapped_column(ForeignKey("users.user_id"))

    options: Mapped[List[PollOptionModel]] = relationship(cascade="all, delete-orphan", lazy="joined")

    @staticmethod
    def create(db: Session, poll_topic: str, creator_id: int, poll_options: List[str]) -> "PollModel":
        poll = PollModel(poll_topic=poll_topic, creator_id=creator_id)
        db.add(poll)
        db.flush()
        for i, option in enumerate(poll_options):
            db.add(PollOptionModel.create(db, poll_id=poll.poll_id, option_num=i, name=option))
        return poll
    
    @staticmethod
    def find(db: Session, poll_id: int) -> Optional["PollModel"]:
        return db.query(PollModel).filter(PollModel.poll_id == poll_id).first()
    
    @staticmethod
    def find_all(db: Session) -> List["PollModel"]:
        return db.query(PollModel).all()
    
    @staticmethod
    def delete(db: Session, poll_id: int) -> bool:
        poll = PollModel.find(db, poll_id)
        if poll is None:
            return False
        db.delete(poll)
        return True
        
