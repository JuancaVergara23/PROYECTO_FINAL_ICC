import pymysql
from typing import List
from models.datalogger import Datalogger
from database.db import get_db_connection

class DataloggerRepository:
    def create(self, datalogger: Datalogger) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Datalogger (ubicacion, nivel_bateria, Clientes_idClientes)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (
                    datalogger.ubicacion,
                    datalogger.nivel_bateria,
                    datalogger.Clientes_idClientes
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idDatalogger: int) -> Datalogger | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Datalogger WHERE idDatalogger = %s"
                cursor.execute(query, (idDatalogger,))
                result = cursor.fetchone()
                return Datalogger(**result) if result else None

    def get_all(self) -> List[Datalogger]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Datalogger")
                results = cursor.fetchall()
                return [Datalogger(**row) for row in results]

    def update(self, idDatalogger: int, datalogger: Datalogger) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Datalogger
                    SET ubicacion = %s, nivel_bateria = %s, Clientes_idClientes = %s
                    WHERE idDatalogger = %s
                """
                cursor.execute(query, (
                    datalogger.ubicacion,
                    datalogger.nivel_bateria,
                    datalogger.Clientes_idClientes,
                    idDatalogger
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idDatalogger: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM Datalogger WHERE idDatalogger = %s"
                cursor.execute(query, (idDatalogger,))
                conn.commit()
                return cursor.rowcount > 0
