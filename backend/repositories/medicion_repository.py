import pymysql
from typing import List
from models.medicion import Medicion
from database.db import get_db_connection

class MedicionRepository:
    def create(self, medicion: Medicion) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Mediciones (
                        humedad, ce, temperatura, n, k, p, fechatiempo,
                        Sensores_idSensores, Sensores_Datalogger_idDatalogger
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    medicion.humedad,
                    medicion.ce,
                    medicion.temperatura,
                    medicion.n,
                    medicion.k,
                    medicion.p,
                    medicion.fechatiempo,
                    medicion.Sensores_idSensores,
                    medicion.Sensores_Datalogger_idDatalogger
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_sensor_id(self, idSensores: int) -> List[Medicion]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM Mediciones
                    WHERE Sensores_idSensores = %s
                    ORDER BY fechatiempo DESC
                """
                cursor.execute(query, (idSensores,))
                results = cursor.fetchall()
                return [Medicion(**row) for row in results]

    def get_by_sensor_and_range(self, idSensores: int, desde: str, hasta: str) -> List[Medicion]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM Mediciones
                    WHERE Sensores_idSensores = %s
                    AND fechatiempo BETWEEN %s AND %s
                    ORDER BY fechatiempo ASC
                """
                cursor.execute(query, (idSensores, desde, hasta))
                results = cursor.fetchall()
                return [Medicion(**row) for row in results]

    def get_all(self) -> List[Medicion]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Mediciones ORDER BY fechatiempo DESC"
                cursor.execute(query)
                results = cursor.fetchall()
                return [Medicion(**row) for row in results]

    def update(self, idMediciones: int, medicion: Medicion) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Mediciones
                    SET humedad = %s, ce = %s, temperatura = %s,
                        n = %s, k = %s, p = %s, fechatiempo = %s,
                        Sensores_idSensores = %s, Sensores_Datalogger_idDatalogger = %s
                    WHERE idMediciones = %s
                """
                cursor.execute(query, (
                    medicion.humedad,
                    medicion.ce,
                    medicion.temperatura,
                    medicion.n,
                    medicion.k,
                    medicion.p,
                    medicion.fechatiempo,
                    medicion.Sensores_idSensores,
                    medicion.Sensores_Datalogger_idDatalogger,
                    idMediciones
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idMediciones: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM Mediciones WHERE idMediciones = %s"
                cursor.execute(query, (idMediciones,))
                conn.commit()
                return cursor.rowcount > 0
