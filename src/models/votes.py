from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
    async def create(db: AsyncSession, poll_id: int, user_id: int, option_num: int) -> "VoteModel":
        vote = VoteModel(poll_id=poll_id, user_id=user_id, option_num=option_num)
        db.add(vote)
        return vote
    
    @staticmethod
    async def find(db: AsyncSession, poll_id: int, user_id: int) -> Optional["VoteModel"]:
        return await db.get(VoteModel, (poll_id, user_id))
    
    async def delete(self, db: AsyncSession):
        await db.delete(self)

    async def update(self, db: AsyncSession, option_num: int):
        self.option_num = option_num
        db.add(self)
        return self