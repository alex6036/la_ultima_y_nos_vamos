from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService

class CLIController:
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService, chatbot_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.current_user = None

    def run(self):
        while True:
            if not self.current_user:
                print("\n1. Registrar usuario")
                print("2. Iniciar sesión")
                print("3. Salir")
                choice = input("Seleccione una opción: ")
                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login_user()
                elif choice == "3":
                    print("¡Adiós!")
                    break
                else:
                    print("Opción no válida.")
            else:
                print("\n1. Crear encuesta")
                print("2. Votar en una encuesta")
                print("3. Ver resultados de una encuesta")
                print("4. Transferir NFT")
                print("5. Ver mis tokens NFT")
                print("6. Hablar con el chatbot")
                print("7. Cerrar sesión")
                print("8. Salir")
                choice = input("Seleccione una opción: ")
                if choice == "1":
                    self.create_poll()
                elif choice == "2":
                    self.vote()
                elif choice == "3":
                    self.view_results()
                elif choice == "4":
                    self.transfer_nft()
                elif choice == "5":
                    self.view_nfts()
                elif choice == "6":
                    self.chat_with_bot()
                elif choice == "7":
                    self.current_user = None
                    print("Sesión cerrada.")
                elif choice == "8":
                    print("¡Adiós!")
                    break
                else:
                    print("Opción no válida.")

    def register_user(self):
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        try:
            self.user_service.register(username, password)
            print(f"Usuario {username} registrado exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")

    def login_user(self):
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        try:
            session_token = self.user_service.login(username, password)
            self.current_user = username
            print("Inicio de sesión exitoso.")
        except ValueError as e:
            print(f"Error: {e}")

    def create_poll(self):
        question = input("Ingrese la pregunta de la encuesta: ")
        options = input("Ingrese las opciones (separadas por comas): ").split(",")
        duration = int(input("Duración en segundos: "))
        poll_type = input("Tipo de encuesta (simple/multiple): ")
        try:
            poll = self.poll_service.create_poll(question, options, duration, poll_type)
            print(f"Encuesta creada exitosamente. ID: {poll.poll_id}")
        except ValueError as e:
            print(f"Error: {e}")

    def vote(self):
        poll_id = input("Ingrese el ID de la encuesta: ")
        option = input("Ingrese la opción a votar: ")
        try:
            self.poll_service.vote(poll_id, self.current_user, option)
            print("Voto registrado exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")

    def view_results(self):
        poll_id = input("Ingrese el ID de la encuesta: ")
        try:
            results = self.poll_service.get_partial_results(poll_id)
            print("Resultados parciales:")
            print("Conteo:", results["counts"])
            print("Porcentajes:", results["percentages"])
        except ValueError as e:
            print(f"Error: {e}")

    def transfer_nft(self):
        token_id = input("Ingrese el ID del token NFT: ")
        new_owner = input("Ingrese el nombre del nuevo propietario: ")
        try:
            self.nft_service.transfer_token(token_id, self.current_user, new_owner)
            print(f"Token {token_id} transferido a {new_owner} exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")

    def view_nfts(self):
        tokens = self.nft_service.get_user_tokens(self.current_user)
        if not tokens:
            print("No tienes tokens NFT.")
        else:
            print("Tus tokens NFT:")
            for token in tokens:
                print(f"Token ID: {token.token_id}, Encuesta: {token.poll_id}, Opción: {token.option}")

    def chat_with_bot(self):
        message = input("Mensaje para el chatbot: ")
        response = self.chatbot_service.respond(message, self.current_user)
        print(f"Chatbot: {response}")