from src.models.token_nft import TokenNFT
from src.repositories.nft_repository import NFTRepository
from src.repositories.usuario_repository import UsuarioRepository

class NFTService:
    def __init__(self, nft_repository, usuario_repository):
        self.nft_repository = nft_repository
        self.usuario_repository = usuario_repository

    def mint_token(self, username, poll_id, option):
        """Genera un nuevo token NFT al votar."""
        print(f"NFTService: mint_token - Generando token para {username}, poll_id={poll_id}, option={option}")
        token = TokenNFT(poll_id, option, username)
        print(f"NFTService: mint_token - Token generado: {token.__dict__}")
        self.nft_repository.save_nft(token)
        print(f"NFTService: mint_token - Token guardado en nfts.json")
        user = self.usuario_repository.get_user(username)
        if user:
            user.add_token(token.token_id)
            self.usuario_repository.save_user(user)
            print(f"NFTService: mint_token - Token {token.token_id} añadido a la lista de {username}")
        else:
            print(f"NFTService: mint_token - Error: Usuario {username} no encontrado")
        return token

    def transfer_token(self, token_id, current_owner, new_owner):
        """Transfiere un token NFT a otro usuario."""
        print(f"Intentando transferir token {token_id} de {current_owner} a {new_owner}")
        token = self.nft_repository.get_nft(token_id)
        if not token:
            print(f"Error: Token {token_id} no encontrado")
            raise ValueError("Token NFT no encontrado.")
        print(f"Token encontrado: {token}")
        if token.owner != current_owner:
            print(f"Error: Propietario actual ({token.owner}) no coincide con {current_owner}")
            raise ValueError("El usuario no es el propietario del token.")
        user_exists = self.usuario_repository.get_user(new_owner)
        if not user_exists:
            print(f"Error: Nuevo propietario {new_owner} no existe")
            raise ValueError("El nuevo propietario no existe.")
        token.owner = new_owner
        print(f"Actualizando propietario del token {token_id} a {new_owner}")
        self.nft_repository.transfer_nft(token_id, new_owner)
        # Actualizar las listas de tokens de los usuarios
        current_user = self.usuario_repository.get_user(current_owner)
        new_user = self.usuario_repository.get_user(new_owner)
        if current_user:
            current_user.remove_token(token_id)
            self.usuario_repository.save_user(current_user)
            print(f"Token {token_id} eliminado de la lista de {current_owner}")
        if new_user:
            new_user.add_token(token_id)
            self.usuario_repository.save_user(new_user)
            print(f"Token {token_id} añadido a la lista de {new_owner}")

    def get_user_tokens(self, username):
        """Obtiene todos los tokens NFT de un usuario."""
        tokens = self.nft_repository.get_nfts_by_owner(username)
        print(f"NFTService: get_user_tokens - Tokens recuperados para {username}: {[token.__dict__ for token in tokens]}")
        return tokens