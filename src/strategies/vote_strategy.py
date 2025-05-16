from datetime import datetime

class DefaultVoteStrategy:
    def vote(self, poll, username, option, weight=1):
        """
        Registra un voto en la encuesta.

        Args:
            poll: Instancia de Poll donde se registra el voto.
            username (str): Nombre del usuario que vota.
            option (str): Opción seleccionada por el usuario.
            weight (float, opcional): Peso del voto (para encuestas weighted). Por defecto es 1.

        Returns:
            None
        """
        poll.add_vote(username, option, weight=weight)