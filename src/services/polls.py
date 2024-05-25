from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.models.polls import PollModel
from src.serializers.polls.poll_creation import PollCreationSerializer
from src.serializers.polls.poll_creation_output import PollCreationOutputSerializer
from src.serializers.polls.poll_preview import PollPreviewSerializer
from src.serializers.polls.full_poll import FullPollSerializer
from src.serializers.polls.all_polls import AllPollsSerializer

class PollsService:
    async def create(self, db: AsyncSession, user_id: int, poll_creation_serializer: PollCreationSerializer) -> PollCreationOutputSerializer:
        if len(poll_creation_serializer.options) < 2:
            raise ValueError("A poll must have at least 2 options")
        
        poll = await PollModel.create(db, poll_creation_serializer.title, user_id, poll_creation_serializer.options)
        return PollCreationOutputSerializer(id=poll.poll_id)
    
    async def delete(self, db: AsyncSession, poll_id: int, requester_id: int):
        poll = await PollModel.find(db, poll_id)
        if not poll:
            raise LookupError("Poll not found")
        if poll.creator_id != requester_id:
            raise ValueError("You are not the creator of this poll")
        
        await PollModel.delete(db, poll_id)
    
    async def get_all(self, db: AsyncSession) -> AllPollsSerializer:
        polls = await PollModel.find_all(db)
        return AllPollsSerializer(polls=[PollPreviewSerializer.from_orm(poll) for poll in polls])
    
    async def get(self, db: AsyncSession, poll_id: int) -> FullPollSerializer | None:
        poll = await PollModel.find(db, poll_id)
        if not poll:
            return None
        return FullPollSerializer.from_model(poll)
    
polls_service = PollsService()