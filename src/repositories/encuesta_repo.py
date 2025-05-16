import json
import os
from src.models.encuesta import Poll
from src.models.voto import Vote
from datetime import datetime

class EncuestaRepository:
    def __init__(self, storage_path, storage_type):
        self.storage_path = storage_path
        self.storage_type = storage_type
        self.polls_file = os.path.join(self.storage_path, "polls.json")
        self.votes_file = os.path.join(self.storage_path, "votes.json")
        self._initialize_storage()

    def _initialize_storage(self):
        if self.storage_type != "json":
            raise NotImplementedError("Solo se soporta almacenamiento JSON por ahora.")
        if not os.path.exists(self.polls_file):
            with open(self.polls_file, "w") as f:
                json.dump([], f)
        if not os.path.exists(self.votes_file):
            with open(self.votes_file, "w") as f:
                json.dump([], f)

    def save_poll(self, poll):
        try:
            with open(self.polls_file, "r") as f:
                polls = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            polls = []
        poll_data = {
            "poll_id": poll.poll_id,
            "question": poll.question,
            "options": poll.options,
            "votes": poll.votes,
            "duration_seconds": poll.duration_seconds,
            "timestamp_start": poll.timestamp_start.isoformat(),
            "poll_type": poll.poll_type,
            "status": poll.status
        }
        for i, existing_poll in enumerate(polls):
            if existing_poll["poll_id"] == poll.poll_id:
                polls[i] = poll_data
                break
        else:
            polls.append(poll_data)
        with open(self.polls_file, "w") as f:
            json.dump(polls, f)

    def get_poll(self, poll_id):
        with open(self.polls_file, "r") as f:
            polls = json.load(f)
        for poll_data in polls:
            if poll_data["poll_id"] == poll_id:
                poll = Poll(
                    poll_id=poll_data["poll_id"],
                    question=poll_data["question"],
                    options=poll_data["options"],
                    duration_seconds=poll_data["duration_seconds"],
                    poll_type=poll_data["poll_type"]
                )
                poll.votes = poll_data.get("votes", {})
                poll.timestamp_start = datetime.fromisoformat(poll_data["timestamp_start"])
                poll.status = poll_data.get("status", "active")
                return poll
        return None

    def has_user_voted(self, poll_id, username):
        with open(self.votes_file, "r") as f:
            votes = json.load(f)
        return any(vote["poll_id"] == poll_id and vote["username"] == username for vote in votes)

    def save_vote(self, vote):
        with open(self.votes_file, "r") as f:
            votes = json.load(f)
        vote_data = {
            "poll_id": vote.poll_id,
            "username": vote.username,
            "option": vote.option,
            "timestamp": vote.timestamp.isoformat()
        }
        votes.append(vote_data)
        with open(self.votes_file, "w") as f:
            json.dump(votes, f)

    def get_all_polls(self):
        with open(self.polls_file, "r") as f:
            polls = json.load(f)
        result = []
        for poll_data in polls:
            poll = Poll(
                poll_id=poll_data["poll_id"],
                question=poll_data["question"],
                options=poll_data["options"],
                duration_seconds=poll_data["duration_seconds"],
                poll_type=poll_data["poll_type"]
            )
            poll.votes = poll_data.get("votes", {})
            poll.timestamp_start = datetime.fromisoformat(poll_data["timestamp_start"])
            poll.status = poll_data.get("status", "active")
            result.append(poll)
        return result

    def get_votes_for_poll(self, poll_id):
        """Recupera todos los votos para una encuesta específica."""
        try:
            with open(self.votes_file, "r") as f:
                votes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            votes = []
        result = []
        for vote_data in votes:
            if vote_data["poll_id"] == poll_id:
                vote = Vote(
                    poll_id=vote_data["poll_id"],
                    username=vote_data["username"],
                    option=vote_data["option"],
                    timestamp=datetime.fromisoformat(vote_data["timestamp"])
                )
                result.append(vote)
        return result