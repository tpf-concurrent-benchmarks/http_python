from typing import List

from src.serializers.polls.poll_preview import PollPreviewSerializer
from src.serializers.poll_options.full_poll_option import FullPollOptionSerializer
from src.models.polls import PollModel

class FullPollSerializer(PollPreviewSerializer):
    options: List[FullPollOptionSerializer]

    @classmethod
    def from_model(cls, poll_model: PollModel) -> "FullPollSerializer":
        base_poll = PollPreviewSerializer.from_orm(poll_model)
        votes_per_option = []
        for option in poll_model.options:
            votes_per_option.append(FullPollOptionSerializer(name=option.name, votes=option.count_votes()))
        return cls(**base_poll.dict(), options=votes_per_option)
        