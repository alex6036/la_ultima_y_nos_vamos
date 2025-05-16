import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, poll_id, option, owner, issued_at=None, token_id=None):
        self.token_id = token_id if token_id is not None else str(uuid.uuid4())
        self.poll_id = poll_id
        self.option = option
        self.owner = owner
        self.issued_at = issued_at or datetime.now()

    def __repr__(self):
        return f"TokenNFT(token_id={self.token_id}, poll_id={self.poll_id}, option={self.option}, owner={self.owner}, issued_at={self.issued_at})"