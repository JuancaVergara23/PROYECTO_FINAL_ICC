import pymysql
from typing import List, Optional
from models.usuario import Usuario, UsuarioConID
from database.db import get_db_connection

class UsuarioRepository:
    def create(self, usuario: Usuario) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Usuarios (nombre, correo, contrasena, Tipo_idTipo)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    usuario.nombre,
                    usuario.correo,
                    usuario.contrasena,
                    usuario.Tipo_idTipo
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idUsuarios: int) -> Optional[UsuarioConID]:
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM Usuarios WHERE idUsuarios = %s"
                cursor.execute(query, (idUsuarios,))
                result = cursor.fetchone()
                return UsuarioConID(**result) if result else None
            
    def get_by_nombre(self, nombre: str) -> Optional[UsuarioConID]:
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM Usuarios WHERE nombre = %s"
                cursor.execute(query, (nombre,))
                result = cursor.fetchone()
                return UsuarioConID(**result) if result else None
            
    def get_by_email(self, correo: str) -> UsuarioConID | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Usuarios WHERE correo = %s"
                cursor.execute(query, (correo,))
                result = cursor.fetchone()
                return UsuarioConID(**result) if result else None

    def get_all(self) -> List[UsuarioConID]:
        with get_db_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Usuarios")
                results = cursor.fetchall()
                return [UsuarioConID(**row) for row in results]

    def update(self, idUsuarios: int, usuario: Usuario) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Usuarios
                    SET nombre = %s, correo = %s, contrasena = %s, Tipo_idTipo = %s
                    WHERE idUsuarios = %s
                """
                cursor.execute(query, (
                    usuario.nombre,
                    usuario.correo,
                    usuario.contrasena,
                    usuario.Tipo_idTipo,
                    idUsuarios
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idUsuarios: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM Usuarios WHERE idUsuarios = %s"
                cursor.execute(query, (idUsuarios,))
                conn.commit()
                return cursor.rowcount > 0
