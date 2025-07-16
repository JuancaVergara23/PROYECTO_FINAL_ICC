from fastapi import HTTPException
from models.medicion import Medicion
from repositories.medicion_repository import MedicionRepository
from typing import List

class MedicionService:
    def __init__(self, repository: MedicionRepository):
        self.repository = repository

    def create_medicion(self, medicion: Medicion) -> int:
        if not medicion.Sensores_idSensores or not medicion.Sensores_Datalogger_idDatalogger:
            raise HTTPException(status_code=400, detail="IDs de sensor y datalogger son obligatorios.")
        return self.repository.create(medicion)

    def get_all_mediciones(self) -> List[Medicion]:
        return self.repository.get_all()

    def get_mediciones_by_sensor(self, idSensores: int) -> List[Medicion]:
        return self.repository.get_by_sensor_id(idSensores)

    def get_mediciones_by_range(self, idSensores: int, desde: str, hasta: str) -> List[Medicion]:
        return self.repository.get_by_sensor_and_range(idSensores, desde, hasta)

    def update_medicion(self, idMediciones: int, medicion: Medicion) -> Medicion:
        success = self.repository.update(idMediciones, medicion)
        if not success:
            raise HTTPException(status_code=404, detail="Medición no encontrada.")
        return medicion

    def delete_medicion(self, idMediciones: int) -> None:
        success = self.repository.delete(idMediciones)
        if not success:
            raise HTTPException(status_code=404, detail="Medición no encontrada.")

def get_medicion_service() -> MedicionService:
    return MedicionService(MedicionRepository())
