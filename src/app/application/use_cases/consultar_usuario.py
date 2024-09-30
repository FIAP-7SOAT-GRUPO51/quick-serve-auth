# application/use_cases/consultar_usuario.py

from isNullOrEmpty.is_null_or_empty import is_null_or_empty

from domain.entities.usuario import Usuario
from domain.interfaces.repositories import IUsuarioRepository


class ConsultarUsuarioUseCase:
    def __init__(self, repo: IUsuarioRepository):
        self.repo = repo

    def execute(self, username: str) -> Usuario:
        usuario = self.repo.obter_usuario_por_username(username)
        return usuario
