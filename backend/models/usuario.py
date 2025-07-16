from pydantic import BaseModel,EmailStr

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    Tipo_idTipo: int

class UsuarioConID(Usuario):
    idUsuarios: int
