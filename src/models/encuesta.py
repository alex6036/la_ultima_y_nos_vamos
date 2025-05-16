from datetime import datetime
import uuid

class Poll:
    def __init__(self, poll_id, question, options, duration_seconds, poll_type="simple"):
        self.poll_id = poll_id if poll_id else str(uuid.uuid4())
        self.question = question
        self.options = options
        self.votes = {}  # Para "simple": {username: option}, para "multiple": {username: [options]}
        self.weights = {}  # Para "weighted": {username: {option: weight}}
        self.status = "active"
        self.timestamp_start = datetime.now()
        self.duration_seconds = duration_seconds
        self.poll_type = poll_type

    def is_active(self):
        if self.status == "closed":
            return False
        elapsed_time = (datetime.now() - self.timestamp_start).total_seconds()
        return elapsed_time < self.duration_seconds

    def add_vote(self, username, option, weight=1):
        """Registra un voto según el tipo de encuesta."""
        if not self.is_active():
            raise ValueError("La encuesta está cerrada.")
        if option not in self.options:
            raise ValueError("Opción inválida.")
        
        if self.poll_type == "simple":
            if username in self.votes:
                raise ValueError("El usuario ya ha votado.")
            self.votes[username] = option
        elif self.poll_type == "multiple":
            if username not in self.votes:
                self.votes[username] = []
            if option not in self.votes[username]:
                self.votes[username].append(option)
        elif self.poll_type == "weighted":
            if username not in self.weights:
                self.weights[username] = {}
            self.weights[username][option] = weight

    def close(self):
        self.status = "closed"

    def get_results(self):
        """Devuelve los resultados según el tipo de encuesta."""
        if self.poll_type in ["simple", "multiple"]:
            results = {option: 0 for option in self.options}
            for votes in self.votes.values():
                if self.poll_type == "simple":
                    results[votes] += 1
                else:  # multiple
                    for vote in votes:
                        results[vote] += 1
            return results
        elif self.poll_type == "weighted":
            results = {option: 0 for option in self.options}
            for user_weights in self.weights.values():
                for option, weight in user_weights.items():
                    results[option] += weight
            return results
        return {option: 0 for option in self.options}