from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.repositories.encuesta_repository import EncuestaRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.nft_repository import NFTRepository
from src.patterns.factory import SimplePollFactory
from src.config import RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO
from src.ui.gradio_ui import GradioUI

def main():
    try:
        # Inicializar repositorios
        encuesta_repo = EncuestaRepository(RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO)
        user_repo = UsuarioRepository(RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO)
        nft_repo = NFTRepository(RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO)

        # Inicializar servicios
        nft_service = NFTService(nft_repo, user_repo)
        poll_service = PollService(encuesta_repo, poll_factory=SimplePollFactory(), nft_service=nft_service)
        user_service = UserService(user_repo)
        chatbot_service = ChatbotService()

        # Inicializar y ejecutar Gradio UI
        gradio_ui = GradioUI(poll_service, user_service, nft_service, chatbot_service, port=7860)
        gradio_ui.launch()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        raise

if __name__ == "__main__":
    main()