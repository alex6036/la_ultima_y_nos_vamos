from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class ChatbotService:
    def __init__(self):
        print("Cargando modelo de chatbot...")
        self.tokenizer = AutoTokenizer.from_pretrained("tanusrich/Mental_Health_Chatbot")
        self.model = AutoModelForCausalLM.from_pretrained("tanusrich/Mental_Health_Chatbot")
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        print("Modelo cargado exitosamente.")

    def respond(self, message, username):
        print(f"ChatbotService: respond - Procesando mensaje de {username}: '{message}'")
        
        if not message or not isinstance(message, str) or message.strip() == "":
            print("ChatbotService: respond - Mensaje inválido, devolviendo respuesta genérica")
            return f"{username}, por favor escribe un mensaje válido."

        prompt = f"Usuario: {message}\nChatbot:"
        try:
            response = self.generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)[0]["generated_text"]
            # Extraer solo la parte relevante del chatbot
            chatbot_reply = response.split("Chatbot:")[-1].strip()
            print(f"ChatbotService: respond - Respuesta generada: {chatbot_reply}")
            return f"{username}, {chatbot_reply}"
        except Exception as e:
            print(f"ChatbotService: respond - Error al generar respuesta: {e}")
            return f"{username}, lo siento, hubo un error al generar la respuesta."
