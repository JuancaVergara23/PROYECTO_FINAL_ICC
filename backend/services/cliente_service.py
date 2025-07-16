from fastapi import HTTPException
from typing import List
from models.cliente import Cliente, ClienteConID
from repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def create_cliente(self, cliente: Cliente) -> int:
        if not cliente.Usuarios_idUsuarios:
            raise HTTPException(status_code=400, detail="El ID del usuario es obligatorio.")
        return self.repository.create(cliente)

    def get_cliente(self, cliente_id: int) -> ClienteConID:
        cliente = self.repository.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
        return cliente

    def get_all_clientes(self) -> List[ClienteConID]:
        return self.repository.get_all()

    def update_cliente(self, cliente_id: int, cliente: Cliente) -> ClienteConID:
        success = self.repository.update(cliente_id, cliente)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
        return self.get_cliente(cliente_id)

    def delete_cliente(self, cliente_id: int) -> None:
        success = self.repository.delete(cliente_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")

def get_cliente_service() -> ClienteService:
    return ClienteService(ClienteRepository())
