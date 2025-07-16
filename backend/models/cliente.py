from pydantic import BaseModel

class Cliente(BaseModel):
    n_dataloggers: int
    Usuarios_idUsuarios: int

class ClienteConID(Cliente):
    idClientes: int

