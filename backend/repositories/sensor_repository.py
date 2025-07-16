import pymysql
from models.sensor import Sensor
from database.db import get_db_connection
from typing import List

class SensorRepository:
    def create(self, sensor: Sensor) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Sensores (tipo, lugar, Datalogger_idDatalogger)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (
                    sensor.tipo,
                    sensor.lugar,
                    sensor.Datalogger_idDatalogger
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idSensores: int) -> Sensor | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Sensores WHERE idSensores = %s"
                cursor.execute(query, (idSensores,))
                result = cursor.fetchone()
                return Sensor(**result) if result else None

    def get_all(self) -> List[Sensor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Sensores")
                results = cursor.fetchall()
                return [Sensor(**row) for row in results]

    def update(self, idSensores: int, sensor: Sensor) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Sensores
                    SET tipo = %s, lugar = %s, Datalogger_idDatalogger = %s
                    WHERE idSensores = %s
                """
                cursor.execute(query, (
                    sensor.tipo,
                    sensor.lugar,
                    sensor.Datalogger_idDatalogger,
                    idSensores
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idSensores: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM Sensores WHERE idSensores = %s"
                cursor.execute(query, (idSensores,))
                conn.commit()
                return cursor.rowcount > 0
