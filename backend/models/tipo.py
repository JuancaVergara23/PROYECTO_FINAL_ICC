from pydantic import BaseModel
from typing import Optional

class Tipo(BaseModel):
    idTipo: Optional[int] = None
    nombre: str
