import json
import os
from threading import Lock
from src.models.token_nft import TokenNFT
from src.config import RUTA_ALMACENAMIENTO, TIPO_ALMACENAMIENTO
from datetime import datetime

class NFTRepository:
    def __init__(self, storage_path, storage_type):
        self.storage_path = storage_path
        self.storage_type = storage_type
        self.nfts_file = os.path.join(self.storage_path, "nfts.json")
        self.lock = Lock()  # Añadir candado
        self._initialize_storage()

    def _initialize_storage(self):
        if self.storage_type != "json":
            raise NotImplementedError("Solo se soporta almacenamiento JSON por ahora.")
        with self.lock:
            if not os.path.exists(self.nfts_file):
                with open(self.nfts_file, "w") as f:
                    json.dump([], f)

    def save_nft(self, nft):
        with self.lock:
            with open(self.nfts_file, "r") as f:
                nfts = json.load(f)
            nft_data = {
                "token_id": nft.token_id,
                "poll_id": nft.poll_id,
                "option": nft.option,
                "owner": nft.owner,
                "issued_at": nft.issued_at.isoformat()
            }
            for i, existing_nft in enumerate(nfts):
                if existing_nft["token_id"] == nft.token_id:
                    nfts[i] = nft_data
                    break
            else:
                nfts.append(nft_data)
            with open(self.nfts_file, "w") as f:
                json.dump(nfts, f)

    def get_nft(self, token_id):
        with self.lock:
            with open(self.nfts_file, "r") as f:
                nfts = json.load(f)
            for nft_data in nfts:
                if nft_data["token_id"] == token_id:
                    return TokenNFT(
                        poll_id=nft_data["poll_id"],
                        option=nft_data["option"],
                        owner=nft_data["owner"],
                        issued_at=datetime.fromisoformat(nft_data["issued_at"]),
                        token_id=nft_data["token_id"]
                    )
            return None

    def get_nfts_by_owner(self, owner):
        with self.lock:
            with open(self.nfts_file, "r") as f:
                nfts = json.load(f)
            result = []
            for nft_data in nfts:
                if nft_data["owner"] == owner:
                    nft = TokenNFT(
                        poll_id=nft_data["poll_id"],
                        option=nft_data["option"],
                        owner=nft_data["owner"],
                        issued_at=datetime.fromisoformat(nft_data["issued_at"]),
                        token_id=nft_data["token_id"]
                    )
                    result.append(nft)
            return result

    def transfer_nft(self, token_id, new_owner):
        with self.lock:
            print(f"Actualizando nfts.json: token {token_id} -> nuevo propietario {new_owner}")
            with open(self.nfts_file, "r") as f:
                nfts = json.load(f)
            for nft_data in nfts:
                if nft_data["token_id"] == token_id:
                    nft_data["owner"] = new_owner
                    print(f"Token {token_id} encontrado y actualizado en memoria")
                    break
            else:
                print(f"Error: Token {token_id} no encontrado en nfts.json")
                raise ValueError("Token NFT no encontrado.")
            with open(self.nfts_file, "w") as f:
                json.dump(nfts, f, indent=2)
            print(f"nfts.json actualizado en disco")

    def get_all_nfts(self):
        with self.lock:
            with open(self.nfts_file, "r") as f:
                nfts = json.load(f)
            result = []
            for nft_data in nfts:
                nft = TokenNFT(
                    poll_id=nft_data["poll_id"],
                    option=nft_data["option"],
                    owner=nft_data["owner"],
                    issued_at=datetime.fromisoformat(nft_data["issued_at"]),
                    token_id=nft_data["token_id"]
                )
                result.append(nft)
            return result