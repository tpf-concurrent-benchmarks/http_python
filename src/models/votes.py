from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Session
from typing import Optional

from src.models import Base

class VoteModel(Base):
    __tablename__ = "votes"

    poll_id = Column(Integer, ForeignKey("polls.poll_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    option_num = Column(Integer)


    __table_args__ = (
        PrimaryKeyConstraint("poll_id", "user_id"),
        ForeignKeyConstraint(["poll_id", "option_num"], ["poll_options.poll_id", "poll_options.option_num"]),
    )
    
    @staticmethod
    def create(db: Session, poll_id: int, user_id: int, option_num: int) -> "VoteModel":
        vote = VoteModel(poll_id=poll_id, user_id=user_id, option_num=option_num)
        db.add(vote)
        db.flush()
        return vote
    
    @staticmethod
    def find(db: Session, poll_id: int, user_id: int) -> Optional["VoteModel"]:
        return db.query(VoteModel).filter(VoteModel.poll_id == poll_id, VoteModel.user_id == user_id).first()
    
    def delete(self, db: Session):
        db.delete(self)

    def update(self, db: Session, option_num: int):
        self.option_num = option_num
        db.add(self)
        return self