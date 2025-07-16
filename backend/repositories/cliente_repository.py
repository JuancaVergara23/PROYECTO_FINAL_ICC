import pymysql
from typing import List, Optional
from models.cliente import Cliente, ClienteConID
from database.db import get_db_connection

class ClienteRepository:
    def create(self, cliente: Cliente) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Clientes (n_dataloggers, Usuarios_idUsuarios)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (
                    cliente.n_dataloggers,
                    cliente.Usuarios_idUsuarios
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idClientes: int) -> Optional[ClienteConID]:
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM Clientes WHERE idClientes = %s"
                cursor.execute(query, (idClientes,))
                result = cursor.fetchone()
                return ClienteConID(**result) if result else None
            
    def get_by_usuario_id(self, usuario_id: int) -> Optional[ClienteConID]:
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM Clientes WHERE Usuarios_idUsuarios = %s"
                cursor.execute(query, (usuario_id,))
                result = cursor.fetchone()
                return ClienteConID(**result) if result else None

    def get_all(self) -> List[ClienteConID]:
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Clientes")
                results = cursor.fetchall()
                return [ClienteConID(**row) for row in results]

    def update(self, idClientes: int, cliente: Cliente) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Clientes
                    SET n_dataloggers = %s WHERE idClientes = %s
                """
                cursor.execute(query, (
                    cliente.n_dataloggers,
                    idClientes
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idClientes: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM Clientes WHERE idClientes = %s"
                cursor.execute(query, (idClientes,))
                conn.commit()
                return cursor.rowcount > 0
