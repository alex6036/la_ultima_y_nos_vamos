from datetime import datetime

class Vote:
    def __init__(self, poll_id, username, option, timestamp=None):
        self.poll_id = poll_id
        self.username = username
        self.option = option
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        return f"Vote(poll_id={self.poll_id}, username={self.username}, option={self.option}, timestamp={self.timestamp})"