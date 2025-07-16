from pydantic import BaseModel
from typing import Optional

class Sensor(BaseModel):
    idSensores: Optional[int] = None
    tipo: Optional[int] = None
    lugar: Optional[str] = None
    Datalogger_idDatalogger: int
