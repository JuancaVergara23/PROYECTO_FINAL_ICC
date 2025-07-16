from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Medicion(BaseModel):
    idMediciones: Optional[int] = None
    humedad: Optional[float] = None
    ce: Optional[float] = None
    temperatura: Optional[float] = None
    n: Optional[float] = None
    k: Optional[float] = None
    p: Optional[float] = None
    fechatiempo: Optional[datetime] = None
    Sensores_idSensores: int
    Sensores_Datalogger_idDatalogger: int
