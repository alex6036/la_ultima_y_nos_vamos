from abc import ABC, abstractmethod

class Observer(ABC):
    """Interfaz para los observadores."""
    @abstractmethod
    def update(self, poll):
        pass

class NFTServiceObserver(Observer):
    """Observador que notifica a NFTService cuando una encuesta se cierra."""
    def __init__(self, nft_service):
        self.nft_service = nft_service

    def update(self, poll):
        print(f"Encuesta {poll.poll_id} cerrada. Notificando a NFTService.")
        # Podríamos añadir lógica adicional, como generar tokens especiales al cerrar

class ChatbotServiceObserver(Observer):
    """Observador que notifica a ChatbotService cuando una encuesta se cierra."""
    def __init__(self, chatbot_service):
        self.chatbot_service = chatbot_service

    def update(self, poll):
        print(f"Encuesta {poll.poll_id} cerrada. Notificando a ChatbotService.")
        # Podríamos hacer que el chatbot anuncie el cierre

class PollServiceSubject:
    """Sujeto que gestiona los observadores y notifica cierres de encuestas."""
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        """Añade un observador a la lista."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Elimina un observador de la lista."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, poll):
        """Notifica a todos los observadores sobre el cierre de una encuesta."""
        for observer in self.observers:
            observer.update(poll)