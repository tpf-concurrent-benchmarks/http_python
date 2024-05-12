from sqlalchemy import ForeignKey
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, Mapped, mapped_column, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.models.poll_options import PollOptionModel
from src.models import Base
from src.models.users import UserModel

class PollModel(Base):
    __tablename__ = "polls"

    poll_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    poll_topic: Mapped[str] = mapped_column()
    creator_id: Mapped["UserModel"] = mapped_column(ForeignKey("users.user_id"))

    options: Mapped[List[PollOptionModel]] = relationship(cascade="all, delete-orphan", lazy="select")

    @staticmethod
    async def create(db: AsyncSession, poll_topic: str, creator_id: int, poll_options: List[str]) -> "PollModel":
        poll = PollModel(poll_topic=poll_topic, creator_id=creator_id)
        db.add(poll)
        await db.flush()
        for i, option in enumerate(poll_options):
            db.add(PollOptionModel.create(db, poll_id=poll.poll_id, option_num=i, name=option))
        return poll
    
    @staticmethod
    async def find(db: AsyncSession, poll_id: int) -> Optional["PollModel"]:
        result = await db.execute(select(PollModel).filter(PollModel.poll_id == poll_id).options(selectinload(PollModel.options)))
        return result.scalars().first()
    
    @staticmethod
    async def find_all(db: AsyncSession) -> List["PollModel"]:
        return (await db.execute(select(PollModel))).scalars().all()
    
    @staticmethod
    async def delete(db: AsyncSession, poll_id: int) -> bool:
        poll = await PollModel.find(db, poll_id)
        if poll is None:
            return False
        await db.delete(poll)
        return True
        
