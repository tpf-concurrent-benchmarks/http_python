from sqlalchemy.orm import Session

from src.models.votes import VoteModel
from src.models.polls import PollModel
from src.serializers.vote import VoteSerializer

class VotesService:
    def vote(self, db: Session, poll_id: int, user_id: int, option_num: int):
        poll = PollModel.find(db, poll_id)
        if not poll:
            raise LookupError("Poll not found")
        if not self._validate_option_number(poll, option_num):
            raise ValueError("Invalid option number")

        prev_vote = VoteModel.find(db, poll_id, user_id)
        if prev_vote:
            if prev_vote.option_num == option_num:
                prev_vote.delete(db)
            else:
                prev_vote.update(db, option_num)
        else:
            VoteModel.create(db, poll_id, user_id, option_num)          

    def _validate_option_number(self, poll: PollModel, option_num: int) -> bool:
        return 0 <= option_num < len(poll.options)

votes_service = VotesService()