# domain/interfaces/repositories.py
from abc import ABC, abstractmethod


class IUsuarioRepository(ABC):
    @abstractmethod
    def obter_usuario_por_username(self, username: str):
        pass

    @abstractmethod
    def cria_usuario(self, username: str, email: str):
        pass
