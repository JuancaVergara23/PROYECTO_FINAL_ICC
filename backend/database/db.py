import pymysql
from contextlib import contextmanager
#localmente
# Database configuration
# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',  # Replace with your MySQL password
#     'database': 'db_agro',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor
# }

#PARA CORRER EN LA NUBE
DB_CONFIG = {
    'host': 'db',  # el nombre del servicio del contenedor MySQL en Docker Compose
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'db_agro',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Database connection context manager

@contextmanager
def get_db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()

# Este init_db debería usarse solo para desarrollo
def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")  # Verifica la conexión
        print("✅ Conexión exitosa a la base de datos.")

# Initialize database
# def init_db():
#     with get_db_connection() as conn:
#         with conn.cursor() as cursor:
#             # Tabla Tipo
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Tipo (
#                     idTipo INT NOT NULL,
#                     nombre VARCHAR(45) NULL,
#                     PRIMARY KEY (idTipo)
#                 )
#             """)

#             # Tabla Usuarios
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Usuarios (
#                     idUsuarios INT NOT NULL,
#                     nombre VARCHAR(45) NULL,
#                     correo VARCHAR(45) NULL,
#                     contrasena VARCHAR(45) NULL,
#                     Tipo_idTipo INT NOT NULL,
#                     PRIMARY KEY (idUsuarios),
#                     FOREIGN KEY (Tipo_idTipo)
#                         REFERENCES Tipo (idTipo)
#                         ON DELETE NO ACTION ON UPDATE NO ACTION
#                 )
#             """)

#             # Tabla Clientes
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Clientes (
#                     idClientes INT NOT NULL,
#                     n_dataloggers INT NULL,
#                     Usuarios_idUsuarios INT NOT NULL,
#                     PRIMARY KEY (idClientes),
#                     FOREIGN KEY (Usuarios_idUsuarios)
#                         REFERENCES Usuarios (idUsuarios)
#                         ON DELETE NO ACTION ON UPDATE NO ACTION
#                 )
#             """)

#             # Tabla Datalogger
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Datalogger (
#                     idDatalogger INT NOT NULL,
#                     ubicacion VARCHAR(45) NULL,
#                     nivel_bateria FLOAT NULL,
#                     Clientes_idClientes INT NOT NULL,
#                     PRIMARY KEY (idDatalogger, Clientes_idClientes),
#                     FOREIGN KEY (Clientes_idClientes)
#                         REFERENCES Clientes (idClientes)
#                         ON DELETE NO ACTION ON UPDATE NO ACTION
#                 )
#             """)

#             # Tabla Sensores
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Sensores (
#                     idSensores INT NOT NULL,
#                     tipo INT NULL,
#                     lugar VARCHAR(45) NULL,
#                     Datalogger_idDatalogger INT NOT NULL,
#                     PRIMARY KEY (idSensores, Datalogger_idDatalogger),
#                     FOREIGN KEY (Datalogger_idDatalogger)
#                         REFERENCES Datalogger (idDatalogger)
#                         ON DELETE NO ACTION ON UPDATE NO ACTION
#                 )
#             """)

#             # Tabla Mediciones
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Mediciones (
#                     idMediciones INT NOT NULL,
#                     humedad FLOAT NULL,
#                     ce FLOAT NULL,
#                     temperatura FLOAT NULL,
#                     n FLOAT NULL,
#                     k FLOAT NULL,
#                     p FLOAT NULL,
#                     fechatiempo DATETIME NULL,
#                     Sensores_idSensores INT NOT NULL,
#                     Sensores_Datalogger_idDatalogger INT NOT NULL,
#                     PRIMARY KEY (idMediciones, Sensores_idSensores, Sensores_Datalogger_idDatalogger),
#                     FOREIGN KEY (Sensores_idSensores, Sensores_Datalogger_idDatalogger)
#                         REFERENCES Sensores (idSensores, Datalogger_idDatalogger)
#                         ON DELETE NO ACTION ON UPDATE NO ACTION
#                 )
#             """)

#             conn.commit()