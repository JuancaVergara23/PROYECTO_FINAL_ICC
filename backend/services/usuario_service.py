from fastapi import HTTPException
from typing import List
from models.usuario import Usuario, UsuarioConID
from repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def create_usuario(self, usuario: Usuario) -> int:
        if not usuario.correo:
            raise HTTPException(status_code=400, detail="El correo es obligatorio.")
        return self.repository.create(usuario)

    def get_usuario(self, usuario_id: int) -> UsuarioConID:
        user = self.repository.get_by_id(usuario_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        return user

    def get_all_usuarios(self) -> List[UsuarioConID]:
        return self.repository.get_all()

    def update_usuario(self, usuario_id: int, usuario: Usuario) -> UsuarioConID:
        success = self.repository.update(usuario_id, usuario)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        return self.get_usuario(usuario_id)

    def delete_usuario(self, usuario_id: int) -> None:
        success = self.repository.delete(usuario_id)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

def get_usuario_service() -> UsuarioService:
    return UsuarioService(UsuarioRepository())
