from models.tipo import Tipo
from typing import List
from database.db import get_db_connection

class TipoRepository:

    def get_all(self) -> List[Tipo]:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Tipo")
        return cursor.fetchall()

    def get_nombre_by_id(self, idTipo: int) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM Tipo WHERE idTipo = %s", (idTipo,))
            row = cursor.fetchone()
            if row:
                return row[0]  # devuelve solo el nombre
            return None