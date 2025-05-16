import uuid
import hashlib

class User:
    def __init__(self, username, password, session_token=None, tokens=None):
        self.username = username
        self.password_hash = self._hash_password(password) if password else None
        self.session_token = session_token
        self.tokens = tokens if tokens is not None else []

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)

    def generate_session_token(self):
        self.session_token = str(uuid.uuid4())
        return self.session_token

    def add_token(self, token_id):
        self.tokens.append(token_id)

    def remove_token(self, token_id):
        if token_id in self.tokens:
            self.tokens.remove(token_id)