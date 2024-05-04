from src.serializers.poll_options.poll_option_creation import PollOptionCreationSerializer

class FullPollOptionSerializer(PollOptionCreationSerializer):
    votes: int