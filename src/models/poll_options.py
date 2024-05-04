from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm.session import Session
from typing import List

from src.models import Base
from src.models.votes import VoteModel

class PollOptionModel(Base):
    __tablename__ = "poll_options"

    poll_id = Column(Integer, ForeignKey("polls.poll_id"))
    option_num = Column(Integer)
    name = Column(String)

    votes: Mapped[List["VoteModel"]] = relationship(cascade="all, delete-orphan", lazy="joined")

    __table_args__ = (
        PrimaryKeyConstraint("poll_id", "option_num"),
        ForeignKeyConstraint(["poll_id"], ["polls.poll_id"]),
    )
    
    @staticmethod
    def create(db: Session, poll_id: int, option_num: int, name: str) -> "PollOptionModel":
        option = PollOptionModel(poll_id=poll_id, option_num=option_num, name=name)
        db.add(option)
        db.flush()
        return option
    
    def count_votes(self) -> int:
        return len(self.votes)