import gradio as gr
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

class GradioUI:
    def __init__(self, poll_service, user_service, nft_service, chatbot_service, port):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.port = port

    def launch(self):
        """Inicia la interfaz web con Gradio."""
        with gr.Blocks() as app:
            gr.Markdown("# Plataforma de Votaciones en Vivo para Streamers")

            # Sección de autenticación
            gr.Markdown("## Autenticación")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Iniciar Sesión")
                    login_username = gr.Textbox(label="Usuario")
                    login_password = gr.Textbox(label="Contraseña", type="password")
                    login_button = gr.Button("Iniciar Sesión")
                    login_output = gr.Textbox(label="Resultado")
                with gr.Column():
                    gr.Markdown("### Registrar Usuario")
                    register_username = gr.Textbox(label="Usuario")
                    register_password = gr.Textbox(label="Contraseña", type="password")
                    register_button = gr.Button("Registrar")
                    register_output = gr.Textbox(label="Resultado")

            # Sección de encuestas
            gr.Markdown("## Encuestas")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Crear Encuesta")
                    question_input = gr.Textbox(label="Pregunta")
                    options_input = gr.Textbox(label="Opciones (separadas por comas)")
                    duration_input = gr.Number(label="Duración (segundos)", value=60)
                    poll_type_input = gr.Dropdown(label="Tipo de Encuesta", choices=["simple", "multiple", "weighted"], value="simple")
                    create_poll_button = gr.Button("Crear Encuesta")
                    create_poll_output = gr.Textbox(label="Resultado")
                with gr.Column():
                    gr.Markdown("### Votar en Encuesta")
                    active_polls = self._get_active_polls()
                    initial_poll = active_polls[0] if active_polls else None
                    poll_list = gr.Dropdown(label="Seleccionar Encuesta", choices=active_polls, value=initial_poll)
                    refresh_polls_button = gr.Button("Refrescar Encuestas")
                    refresh_options_button = gr.Button("Refrescar Opciones")
                    initial_options = self.get_poll_options(initial_poll) if initial_poll else []
                    option_input = gr.Dropdown(label="Opción", choices=initial_options, value=None, allow_custom_value=True)
                    weight_input = gr.Number(label="Peso del Voto (solo para encuestas ponderadas)", value=1)
                    vote_button = gr.Button("Votar")
                    vote_output = gr.Textbox(label="Resultado del Voto")

            # Sección de resultados
            gr.Markdown("## Resultados de la Encuesta")
            results_table = gr.Dataframe(
                label="Resultados",
                headers=["Opción", "Porcentaje (%)"],
                value=[]  # Inicialmente vacío
            )

            # Sección de chatbot
            gr.Markdown("## Chatbot")
            chatbot_input = gr.Textbox(label="Pregunta")
            chatbot_output = gr.Textbox(label="Respuesta")
            chatbot_button = gr.Button("Enviar Pregunta")

            # Sección de tokens
            gr.Markdown("## Tus Tokens NFT")
            token_list = gr.Dataframe(label="Tus Tokens", headers=["Token ID", "Encuesta", "Opción"])
            transfer_token_id = gr.Textbox(label="ID del Token a Transferir")
            transfer_new_owner = gr.Textbox(label="Nuevo Propietario")
            transfer_button = gr.Button("Transferir Token")
            transfer_output = gr.Textbox(label="Resultado de la Transferencia")

            # Conectar eventos
            register_button.click(self.register, inputs=[register_username, register_password], outputs=register_output)
            login_button.click(self.login, inputs=[login_username, login_password], outputs=login_output).then(
                self.view_tokens, inputs=[login_username, login_output], outputs=token_list
            )
            create_poll_button.click(self.create_poll, inputs=[question_input, options_input, duration_input, poll_type_input, login_output, login_username], outputs=[create_poll_output, poll_list, option_input]).then(
                self.get_poll_results, inputs=[poll_list], outputs=results_table
            )
            refresh_polls_button.click(self.refresh_polls, inputs=[], outputs=[poll_list, option_input]).then(
                self.get_poll_results, inputs=[poll_list], outputs=results_table
            )
            refresh_options_button.click(self.refresh_options, inputs=[poll_list], outputs=option_input).then(
                self.get_poll_results, inputs=[poll_list], outputs=results_table
            )
            poll_list.change(self.get_poll_options_for_update, inputs=[poll_list], outputs=option_input).then(
                self.get_poll_results, inputs=[poll_list], outputs=results_table
            )
            vote_button.click(self.vote, inputs=[poll_list, login_username, option_input, weight_input, login_output], outputs=[vote_output, token_list]).then(
                self.get_poll_results, inputs=[poll_list], outputs=results_table
            )
            login_username.change(self.view_tokens, inputs=[login_username, login_output], outputs=token_list)
            transfer_button.click(self.transfer, inputs=[transfer_token_id, transfer_new_owner, login_username, login_output], outputs=[transfer_output, token_list])
            chatbot_button.click(self.chat, inputs=[chatbot_input, login_username, login_output], outputs=chatbot_output)

        app.launch(server_port=self.port)

    def _get_active_polls(self):
        """Devuelve una lista de IDs de encuestas activas."""
        print("Gradio: _get_active_polls - Obteniendo encuestas activas")
        polls = self.poll_service.encuesta_repository.get_all_polls()
        active_polls = [poll.poll_id for poll in polls if poll.is_active()]
        print(f"Gradio: _get_active_polls - Encuestas activas: {active_polls}")
        return active_polls

    def get_poll_options(self, poll_id):
        """Obtiene las opciones de una encuesta dada su poll_id."""
        print(f"Gradio: get_poll_options - Obteniendo opciones para poll_id={poll_id}")
        if not poll_id:
            print("Gradio: get_poll_options - No se proporcionó poll_id, devolviendo lista vacía")
            return []
        poll = self.poll_service.encuesta_repository.get_poll(poll_id)
        if poll:
            print(f"Gradio: get_poll_options - Encuesta encontrada: {poll.__dict__}")
            print(f"Gradio: get_poll_options - Opciones devueltas: {poll.options}")
            return poll.options
        else:
            print(f"Gradio: get_poll_options - Encuesta no encontrada: {poll_id}")
            return []

    def get_poll_options_for_update(self, poll_id):
        """Obtiene las opciones de una encuesta y las devuelve en formato gr.update."""
        options = self.get_poll_options(poll_id)
        print(f"Gradio: get_poll_options_for_update - Actualizando option_input con opciones: {options}")
        return gr.update(choices=options, value=None)

    def get_poll_results(self, poll_id):
        """Obtiene los resultados de una encuesta y los formatea como tabla."""
        print(f"Gradio: get_poll_results - Obteniendo resultados para poll_id={poll_id}")
        if not poll_id:
            print("Gradio: get_poll_results - No se proporcionó poll_id, devolviendo tabla vacía")
            return []
        try:
            results = self.poll_service.get_partial_results(poll_id)
            percentages = results["percentages"]
            result_table = [[option, f"{percentage:.1f}"] for option, percentage in percentages.items()]
            print(f"Gradio: get_poll_results - Resultados formateados: {result_table}")
            return result_table
        except ValueError as e:
            print(f"Gradio: get_poll_results - Error: {e}")
            return []

    def register(self, username, password):
        try:
            user = self.user_service.register(username, password)
            return f"Usuario {username} registrado exitosamente."
        except ValueError as e:
            return f"Error: {e}"

    def login(self, username, password):
        try:
            session_token = self.user_service.login(username, password)
            return f"Sesión iniciada con éxito. Token: {session_token}"
        except ValueError as e:
            return f"Error: {e}"

    def create_poll(self, question, options, duration, poll_type, login_output, username):
        print(f"Gradio: create_poll - Creando encuesta: question={question}, options={options}, duration={duration}, poll_type={poll_type}, username={username}")
        if not login_output or not login_output.startswith("Sesión iniciada"):
            print("Gradio: create_poll - Sesión no iniciada")
            return "Debes iniciar sesión primero.", self._get_active_polls(), gr.update(choices=[], value=None)
        try:
            session_token = login_output.split("Token: ")[1]
            print(f"Gradio: create_poll - Verificando sesión para {username} con token {session_token}")
            self.user_service.verify_session(username, session_token)
            options_list = [opt.strip() for opt in options.split(",")]
            poll = self.poll_service.create_poll(question, options_list, int(duration), poll_type)
            print(f"Gradio: create_poll - Encuesta creada: {poll.__dict__}")
            active_polls = self._get_active_polls()
            new_poll_id = poll.poll_id
            new_options = self.get_poll_options(new_poll_id)
            print(f"Gradio: create_poll - Actualizando poll_list con: {active_polls}, seleccionando: {new_poll_id}")
            print(f"Gradio: create_poll - Actualizando option_input con opciones: {new_options}")
            return f"Encuesta creada exitosamente. ID: {poll.poll_id}", gr.update(choices=active_polls, value=new_poll_id), gr.update(choices=new_options, value=None)
        except (ValueError, IndexError) as e:
            print(f"Gradio: create_poll - Error: {e}")
            return f"Error: {e}", self._get_active_polls(), gr.update(choices=[], value=None)

    def refresh_polls(self):
        print("Gradio: refresh_polls - Refrescando lista de encuestas")
        active_polls = self._get_active_polls()
        print(f"Gradio: refresh_polls - Encuestas activas: {active_polls}")
        initial_poll = active_polls[0] if active_polls else None
        initial_options = self.get_poll_options(initial_poll) if initial_poll else []
        print(f"Gradio: refresh_polls - Seleccionando poll_id: {initial_poll}, opciones: {initial_options}")
        return gr.update(choices=active_polls, value=initial_poll), gr.update(choices=initial_options, value=None)

    def refresh_options(self, poll_id):
        print(f"Gradio: refresh_options - Refrescando opciones para poll_id={poll_id}")
        options = self.get_poll_options(poll_id)
        print(f"Gradio: refresh_options - Opciones actualizadas: {options}")
        return gr.update(choices=options, value=None)

    def vote(self, poll_id, username, option, weight, login_output):
        print(f"Gradio: vote - Iniciando votación: poll_id={poll_id}, username={username}, option={option}, weight={weight}, login_output={login_output}")
        if not login_output or not login_output.startswith("Sesión iniciada"):
            print("Gradio: vote - Sesión no iniciada")
            return "Debes iniciar sesión primero.", gr.update(value=[])
        try:
            session_token = login_output.split("Token: ")[1]
            print(f"Gradio: vote - Verificando sesión para {username} con token {session_token}")
            self.user_service.verify_session(username, session_token)
            print(f"Gradio: vote - Sesión verificada, intentando votar")
            self.poll_service.vote(poll_id, username, option, weight)
            print(f"Gradio: vote - Voto registrado exitosamente para {username} en {poll_id}")
            # Actualizar token_list después de votar
            tokens = self.nft_service.get_user_tokens(username)
            updated_tokens = [[token.token_id, token.poll_id, token.option] for token in tokens]
            print(f"Gradio: vote - Tokens actualizados para {username}: {updated_tokens}")
            return f"Voto registrado para {username} en la encuesta {poll_id}.", updated_tokens
        except (ValueError, IndexError) as e:
            print(f"Gradio: vote - Error: {e}")
            return f"Error: {e}", gr.update(value=[])

    def chat(self, message, username, login_output):
        print(f"Gradio: chat - Procesando mensaje para usuario {username}: '{message}'")
        print(f"Gradio: chat - Estado de autenticación: login_output='{login_output}'")
        if not login_output or not login_output.startswith("Sesión iniciada"):
            print("Gradio: chat - Sesión no iniciada, devolviendo mensaje de error")
            return "Debes iniciar sesión primero."
        try:
            session_token = login_output.split("Token: ")[1]
            print(f"Gradio: chat - Verificando sesión para {username} con token {session_token}")
            self.user_service.verify_session(username, session_token)
            print(f"Gradio: chat - Sesión verificada, enviando mensaje al ChatbotService")
            response = self.chatbot_service.respond(message, username)
            print(f"Gradio: chat - Respuesta recibida: {response}")
            return response
        except (ValueError, IndexError) as e:
            print(f"Gradio: chat - Error en verificación de sesión: {e}")
            return f"Error: {e}"

    def view_tokens(self, username, login_output):
        print(f"Gradio: view_tokens - Username: {username}, Login Output: {login_output}")
        if not login_output or not login_output.startswith("Sesión iniciada"):
            print("Gradio: view_tokens - Sesión no iniciada, devolviendo lista vacía")
            return gr.update(value=[])
        try:
            session_token = login_output.split("Token: ")[1]
            print(f"Gradio: view_tokens - Verificando sesión para {username} con token {session_token}")
            if self.user_service.verify_session(username, session_token):
                print(f"Gradio: view_tokens - Sesión válida, recuperando tokens para {username}")
                tokens = self.nft_service.get_user_tokens(username)
                updated_tokens = [[token.token_id, token.poll_id, token.option] for token in tokens]
                print(f"Gradio: view_tokens - Tokens recuperados: {updated_tokens}")
                return updated_tokens
            else:
                print("Gradio: view_tokens - Sesión inválida, devolviendo lista vacía")
                return gr.update(value=[])
        except (ValueError, IndexError) as e:
            print(f"Gradio: view_tokens - Error: {e}, devolviendo lista vacía")
            return gr.update(value=[])

    def transfer(self, token_id, new_owner, username, login_output):
        print(f"Gradio: Intentando transferir token {token_id} de {username} a {new_owner}")
        if not login_output or not login_output.startswith("Sesión iniciada"):
            return "Debes iniciar sesión primero.", []
        try:
            session_token = login_output.split("Token: ")[1]
            self.user_service.verify_session(username, session_token)
            self.nft_service.transfer_token(token_id, username, new_owner)
            tokens = self.nft_service.get_user_tokens(username)
            return f"Token {token_id} transferido a {new_owner}.", [[token.token_id, token.poll_id, token.option] for token in tokens]
        except (ValueError, IndexError) as e:
            print(f"Gradio: Error en transferencia: {e}")
            return f"Error: {e}", []