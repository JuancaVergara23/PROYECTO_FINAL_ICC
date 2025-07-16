from fastapi import HTTPException
from models.datalogger import Datalogger
from repositories.datalogger_repository import DataloggerRepository
from repositories.cliente_repository import ClienteRepository
from typing import List

class DataloggerService:
    def __init__(self, repository: DataloggerRepository):
        self.repository = repository
        self.cliente_repo = ClienteRepository()

    def create_datalogger(self, datalogger: Datalogger) -> int:
        if not datalogger.Clientes_idClientes:
            raise HTTPException(status_code=400, detail="El ID del cliente es obligatorio.")
        
        # 1. Crear datalogger
        nuevo_id = self.repository.create(datalogger)

        # 2. Obtener cliente
        cliente = self.cliente_repo.get_by_id(datalogger.Clientes_idClientes)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")

        # 3. Incrementar n_dataloggers
        cliente.n_dataloggers += 1
        self.cliente_repo.update(cliente.idClientes, cliente)
        return nuevo_id

    def get_datalogger(self, datalogger_id: int) -> Datalogger:
        dato = self.repository.get_by_id(datalogger_id)
        if not dato:
            raise HTTPException(status_code=404, detail="Datalogger no encontrado.")
        return dato

    def get_all_dataloggers(self) -> List[Datalogger]:
        return self.repository.get_all()

    def update_datalogger(self, datalogger_id: int, datalogger: Datalogger) -> Datalogger:
        success = self.repository.update(datalogger_id, datalogger)
        if not success:
            raise HTTPException(status_code=404, detail="Datalogger no encontrado.")
        return self.get_datalogger(datalogger_id)

    def delete_datalogger(self, datalogger_id: int) -> None:
        success = self.repository.delete(datalogger_id)
        if not success:
            raise HTTPException(status_code=404, detail="Datalogger no encontrado.")

def get_datalogger_service() -> DataloggerService:
    return DataloggerService(DataloggerRepository())
