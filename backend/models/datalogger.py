from pydantic import BaseModel
from typing import Optional

class Datalogger(BaseModel):
    idDatalogger: Optional[int] = None
    ubicacion: Optional[str] = None
    nivel_bateria: Optional[float] = None
    Clientes_idClientes: int
