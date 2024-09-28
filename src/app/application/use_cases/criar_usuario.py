# application/use_cases/consultar_usuario.py

from isNullOrEmpty.is_null_or_empty import is_null_or_empty

from domain.entities.usuario import Usuario
from domain.interfaces.repositories import IUsuarioRepository


class CriarUsuarioUseCase:
    def __init__(self, repo: IUsuarioRepository):
        self.repo = repo

    def execute(self, username: str, email: str) -> Usuario:
        usuario = self.repo.cria_usuario(username, email)
        if is_null_or_empty(usuario.username):
            raise Exception("Erro ao criar usuario.")
        return usuario
