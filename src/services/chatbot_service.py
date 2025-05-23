class ChatbotService:
    def __init__(self):
        self.responses = {
            "hola": "¡Hola! ¿En qué puedo ayudarte?",
            "cómo estás": "Estoy bien, gracias por preguntar. ¿Y tú?",
            "adiós": "¡Hasta luego! Que tengas un buen día.",
            "qué tal": "Todo bien por aquí, ¿y tú qué tal?",
            "gracias": "De nada, ¡siempre estoy aquí para ayudar!"
        }

    def respond(self, message, username):
        print(f"ChatbotService: respond - Procesando mensaje de {username}: '{message}'")
        if not message or not isinstance(message, str):
            print("ChatbotService: respond - Mensaje inválido, devolviendo respuesta genérica")
            return f"{username}, por favor escribe un mensaje válido."
        message = message.lower().strip()
        for key in self.responses:
            if key in message:
                response = f"{username}, {self.responses[key]}"
                print(f"ChatbotService: respond - Respuesta generada: {response}")
                return response
        response = f"{username}, no entiendo tu mensaje. ¿Puedes reformularlo?"
        print(f"ChatbotService: respond - Respuesta genérica: {response}")
        return response