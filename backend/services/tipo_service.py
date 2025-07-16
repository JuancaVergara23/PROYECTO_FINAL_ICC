from repositories.tipo_repository import TipoRepository
from typing import Optional

class TipoService:
    def __init__(self):
        self.repository = TipoRepository()

    def get_all_tipos(self):
        return self.repository.get_all()

    def obtener_nombre_tipo(self, id_tipo: int) -> Optional[str]:
        return self.repository.get_nombre_by_id(id_tipo)