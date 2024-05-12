from sqlalchemy.ext.asyncio import AsyncSession

from src.models.votes import VoteModel
from src.models.polls import PollModel

class VotesService:
    async def vote(self, db: AsyncSession, poll_id: int, user_id: int, option_num: int):
        prev_vote = await VoteModel.find(db, poll_id, user_id)
        if prev_vote:
            if prev_vote.option_num == option_num:
                await prev_vote.delete(db)
            else:
                await prev_vote.update(db, option_num)
        else:
            await VoteModel.create(db, poll_id, user_id, option_num)          

    def _validate_option_number(self, poll: PollModel, option_num: int) -> bool:
        return 0 <= option_num < len(poll.options)

votes_service = VotesService()