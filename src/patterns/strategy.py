from abc import ABC, abstractmethod
import random

class DesempateStrategy(ABC):
    """Interfaz para las estrategias de desempate."""
    @abstractmethod
    def resolve(self, poll):
        pass

class AlphabeticalStrategy(DesempateStrategy):
    """Elige la primera opción alfabéticamente en caso de empate."""
    def resolve(self, poll):
        results = poll.get_results()
        max_votes = max(results.values())
        winners = [option for option, count in results.items() if count == max_votes]
        return min(winners)  # Elige la primera opción alfabéticamente

class RandomStrategy(DesempateStrategy):
    """Elige una opción al azar en caso de empate."""
    def resolve(self, poll):
        results = poll.get_results()
        max_votes = max(results.values())
        winners = [option for option, count in results.items() if count == max_votes]
        return random.choice(winners)  # Elige una opción al azar

class ExtensionStrategy(DesempateStrategy):
    """Extiende la duración de la encuesta en caso de empate."""
    def resolve(self, poll):
        # Simula una prórroga duplicando la duración de la encuesta
        poll.duration_seconds *= 2
        poll.status = "active"
        poll.timestamp_start = datetime.now()  # Reinicia el tiempo para la prórroga
        return None  # Indica que no hay ganador aún