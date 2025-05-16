import json
import os
from threading import Lock
from src.models.usuario import User
from datetime import datetime

class UsuarioRepository:
    def __init__(self, storage_path, storage_type):
        self.storage_path = storage_path
        self.storage_type = storage_type
        self.users_file = os.path.join(self.storage_path, "users.json")
        self.lock = Lock()  # Añadir candado
        self._initialize_storage()

    def _initialize_storage(self):
        if self.storage_type != "json":
            raise NotImplementedError("Solo se soporta almacenamiento JSON por ahora.")
        with self.lock:
            if not os.path.exists(self.users_file):
                with open(self.users_file, "w") as f:
                    json.dump([], f)

    def save_user(self, user):
        with self.lock:
            print(f"Guardando usuario {user.username} en users.json")
            with open(self.users_file, "r") as f:
                users = json.load(f)
            user_data = {
                "username": user.username,
                "password_hash": user.password_hash,
                "session_token": user.session_token,
                "tokens": user.tokens
            }
            for i, existing_user in enumerate(users):
                if existing_user["username"] == user.username:
                    users[i] = user_data
                    break
            else:
                users.append(user_data)
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=2)
            print(f"Usuario {user.username} guardado con tokens: {user.tokens}")

    def get_user(self, username):
        with self.lock:
            with open(self.users_file, "r") as f:
                users = json.load(f)
            for user_data in users:
                if user_data["username"] == username:
                    user = User(
                        username=user_data["username"],
                        password="",
                        session_token=user_data.get("session_token"),
                        tokens=user_data.get("tokens", [])
                    )
                    user.password_hash = user_data["password_hash"]
                    return user
            return None

    def user_exists(self, username):
        with self.lock:
            with open(self.users_file, "r") as f:
                users = json.load(f)
            return any(user["username"] == username for user in users)

    def get_all_users(self):
        with self.lock:
            with open(self.users_file, "r") as f:
                users = json.load(f)
            result = []
            for user_data in users:
                user = User(
                    username=user_data["username"],
                    password="",
                    session_token=user_data.get("session_token"),
                    tokens=user_data.get("tokens", [])
                )
                user.password_hash = user_data["password_hash"]
                result.append(user)
            return result