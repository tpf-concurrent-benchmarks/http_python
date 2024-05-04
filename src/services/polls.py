from sqlalchemy.orm import Session
from typing import List

from src.models.polls import PollModel
from src.serializers.polls.poll_creation import PollCreationSerializer
from src.serializers.polls.poll_creation_output import PollCreationOutputSerializer
from src.serializers.polls.poll_preview import PollPreviewSerializer
from src.serializers.polls.full_poll import FullPollSerializer
from src.serializers.poll_options.full_poll_option import FullPollOptionSerializer

class PollsService:
    def create(self, db: Session, user_id: int, poll_creation_serializer: PollCreationSerializer) -> PollCreationOutputSerializer:
        if len(poll_creation_serializer.options) < 2:
            raise ValueError("A poll must have at least 2 options")
        
        poll = PollModel.create(db, poll_creation_serializer.poll_topic, user_id, poll_creation_serializer.options)
        return PollCreationOutputSerializer(poll_id=poll.poll_id, poll_topic=poll.poll_topic, options=poll_creation_serializer.options)
    
    def delete(self, db: Session, poll_id: int, requester_id: int):
        poll = PollModel.find(db, poll_id)
        if not poll:
            raise LookupError("Poll not found")
        if poll.creator_id != requester_id:
            raise ValueError("You are not the creator of this poll")
        
        PollModel.delete(db, poll_id)
    
    def get_all(self, db: Session) -> List[PollPreviewSerializer]:
        polls = PollModel.find_all(db)
        return [PollPreviewSerializer.from_orm(poll) for poll in polls]
    
    def get(self, db: Session, poll_id: int) -> FullPollSerializer | None:
        poll = PollModel.find(db, poll_id)
        if not poll:
            return None
        return FullPollSerializer.from_model(poll)
    
polls_service = PollsService()