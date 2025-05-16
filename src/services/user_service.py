from src.repositories.usuario_repository import UsuarioRepository
from src.models.usuario import User

class UserService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def register(self, username, password):
        if self.usuario_repository.user_exists(username):
            raise ValueError("El nombre de usuario ya existe.")
        user = User(username, password)
        self.usuario_repository.save_user(user)
        return user

    def login(self, username, password):
        user = self.usuario_repository.get_user(username)
        if not user or not user.verify_password(password):
            raise ValueError("Credenciales inválidas.")
        session_token = user.generate_session_token()
        self.usuario_repository.save_user(user)
        return session_token

    def verify_session(self, username, session_token):
        user = self.usuario_repository.get_user(username)
        if not user:
            return False
        return user.session_token == session_token