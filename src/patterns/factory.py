from src.models.encuesta import Poll

class SimplePollFactory:
    def create_poll(self, poll_id, question, options, duration_seconds, poll_type="simple"):
        """
        Crea una encuesta de tipo simple.

        Args:
            poll_id (str): ID de la encuesta (puede ser None para generar uno automáticamente).
            question (str): Pregunta de la encuesta.
            options (list): Lista de opciones para votar.
            duration_seconds (int): Duración de la encuesta en segundos.
            poll_type (str, opcional): Tipo de encuesta (por defecto "simple").

        Returns:
            Poll: Instancia de la encuesta creada.
        """
        return Poll(poll_id, question, options, duration_seconds, poll_type="simple")

class MultiplePollFactory:
    def create_poll(self, poll_id, question, options, duration_seconds, poll_type="multiple"):
        """
        Crea una encuesta de tipo múltiple (permite múltiples votos por usuario).

        Args:
            poll_id (str): ID de la encuesta (puede ser None para generar uno automáticamente).
            question (str): Pregunta de la encuesta.
            options (list): Lista de opciones para votar.
            duration_seconds (int): Duración de la encuesta en segundos.
            poll_type (str, opcional): Tipo de encuesta (por defecto "multiple").

        Returns:
            Poll: Instancia de la encuesta creada.
        """
        return Poll(poll_id, question, options, duration_seconds, poll_type="multiple")