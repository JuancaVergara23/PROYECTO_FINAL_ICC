from fastapi import FastAPI, Depends, Query,HTTPException
from models.sensor import Sensor
from models.usuario import Usuario
from models.medicion import Medicion
from models.datalogger import Datalogger
from models.cliente import ClienteConID,Cliente

from services.cliente_service import ClienteService, get_cliente_service
from services.sensor_service import SensorService, get_sensor_service
#from services.usuario_service import UsuarioService, get_usuario_service
from services.medicion_service import MedicionService, get_medicion_service
from services.datalogger_service import DataloggerService, get_datalogger_service

from pydantic import BaseModel
from repositories.usuario_repository import UsuarioRepository
from repositories.cliente_repository import ClienteRepository

from database.db import init_db
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request


app = FastAPI()

# Montar carpeta de archivos estáticos (si luego usas CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar ubicación de plantillas HTML
templates = Jinja2Templates(directory="templates")

# Configuración de CORS (permite solicitudes desde un frontend local por ejemplo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambiar según el frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos al arrancar
init_db()

# -------------------------------------------
# ENDPOINT INICIAL
# -------------------------------------------
@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -------------------------------------------
# ENDPOINTS CLIENTES
# -------------------------------------------

@app.get("/api/clientes", response_model=List[ClienteConID])
def listar_clientes(service: ClienteService = Depends(get_cliente_service)):
    return service.get_all_clientes()

@app.delete("/api/clientes/{idCliente}")
def eliminar_cliente(idCliente: int, service: ClienteService = Depends(get_cliente_service)):
    service.delete_cliente(idCliente)
    return {"mensaje": f"Cliente {idCliente} eliminado correctamente"}


# -------------------------------------------
# ENDPOINTS DATALOGGER
# -------------------------------------------

@app.post("/api/dataloggers", status_code=201)
def crear_datalogger(datalogger: Datalogger, service: DataloggerService = Depends(get_datalogger_service)):
    id_creado = service.create_datalogger(datalogger)
    return {"mensaje": "Datalogger registrado", "id": id_creado}

@app.get("/api/dataloggers", response_model=List[Datalogger])
def listar_dataloggers(service: DataloggerService = Depends(get_datalogger_service)):
    return service.get_all_dataloggers()

@app.get("/api/dataloggers/{datalogger_id}", response_model=Datalogger)
def obtener_datalogger(datalogger_id: int, service: DataloggerService = Depends(get_datalogger_service)):
    return service.get_datalogger(datalogger_id)

@app.put("/api/dataloggers/{datalogger_id}")
def actualizar_datalogger(datalogger_id: int, datalogger: Datalogger, service: DataloggerService = Depends(get_datalogger_service)):
    actualizado = service.update_datalogger(datalogger_id, datalogger)
    return {"mensaje": "Datalogger actualizado", "datalogger": actualizado}

@app.delete("/api/dataloggers/{datalogger_id}")
def eliminar_datalogger(datalogger_id: int, service: DataloggerService = Depends(get_datalogger_service)):
    service.delete_datalogger(datalogger_id)
    return {"mensaje": "Datalogger eliminado correctamente"}

# -------------------------------------------
# ENDPOINTS SENSORES
# -------------------------------------------

@app.post("/api/sensores", status_code=201)
def crear_sensor(sensor: Sensor, service: SensorService = Depends(get_sensor_service)):
    sensor_id = service.create_sensor(sensor)
    return {"mensaje": "Sensor registrado correctamente", "id": sensor_id}

@app.get("/api/sensores", response_model=List[Sensor])
def listar_sensores(service: SensorService = Depends(get_sensor_service)):
    return service.get_all_sensors()

@app.get("/api/sensores/{sensor_id}", response_model=Sensor)
def obtener_sensor(sensor_id: int, service: SensorService = Depends(get_sensor_service)):
    return service.get_sensor(sensor_id)

@app.put("/api/sensores/{sensor_id}")
def actualizar_sensor(sensor_id: int, sensor: Sensor, service: SensorService = Depends(get_sensor_service)):
    actualizado = service.update_sensor(sensor_id, sensor)
    return {"mensaje": "Sensor actualizado", "sensor": actualizado}

@app.delete("/api/sensores/{sensor_id}")
def eliminar_sensor(sensor_id: int, service: SensorService = Depends(get_sensor_service)):
    service.delete_sensor(sensor_id)
    return {"mensaje": f"Sensor {sensor_id} eliminado correctamente"}

# -------------------------------------------
# ENDPOINTS MEDICIONES
# -------------------------------------------

@app.post("/api/mediciones", status_code=201)
def registrar_medicion(medicion: Medicion, service: MedicionService = Depends(get_medicion_service)):
    medicion_id = service.create_medicion(medicion)
    return {"mensaje": "Medición registrada", "id": medicion_id}

@app.get("/api/mediciones", response_model=List[Medicion])
def obtener_todas_las_mediciones(service: MedicionService = Depends(get_medicion_service)):
    return service.get_all_mediciones()

@app.get("/api/mediciones/sensor/{sensor_id}", response_model=List[Medicion])
def obtener_mediciones_por_sensor(sensor_id: int, service: MedicionService = Depends(get_medicion_service)):
    return service.get_mediciones_by_sensor(sensor_id)

@app.get("/api/mediciones/sensor/{sensor_id}/rango", response_model=List[Medicion])
def obtener_mediciones_rango(sensor_id: int,
                             desde: str = Query(..., description="Formato: YYYY-MM-DD"),
                             hasta: str = Query(..., description="Formato: YYYY-MM-DD"),
                             service: MedicionService = Depends(get_medicion_service)):
    return service.get_mediciones_by_range(sensor_id, desde, hasta)

@app.put("/api/mediciones/{medicion_id}")
def actualizar_medicion(medicion_id: int, medicion: Medicion, service: MedicionService = Depends(get_medicion_service)):
    actualizado = service.update_medicion(medicion_id, medicion)
    return {"mensaje": "Medición actualizada", "medicion": actualizado}

@app.delete("/api/mediciones/{medicion_id}")
def eliminar_medicion(medicion_id: int, service: MedicionService = Depends(get_medicion_service)):
    service.delete_medicion(medicion_id)
    return {"mensaje": "Medición eliminada correctamente"}

# -------------------------------------------
# FRONTEND
# -------------------------------------------

# -------------------------------------------
# Login Cliente
# -------------------------------------------

# Modelo auxiliar para el login
class LoginRequest(BaseModel):
    correo: str
    contrasena: str

@app.get("/login")
def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(credentials: LoginRequest):
    repo = UsuarioRepository()
    usuario = repo.get_by_email(credentials.correo)

    if not usuario:
        raise HTTPException(status_code=401, detail="Correo no encontrado")

    if usuario.contrasena != credentials.contrasena:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Redirección basada en tipo de usuario
    if usuario.Tipo_idTipo == 1:
        return {"mensaje": "Inicio de sesión exitoso", "nombre": usuario.nombre, "tipo": "admin"}
    elif usuario.Tipo_idTipo == 2:
        return {"mensaje": "Inicio de sesión exitoso", "nombre": usuario.nombre, "tipo": "cliente"}
    else:
        raise HTTPException(status_code=403, detail="Tipo de usuario no válido")
    
# REGISTRO DE UN NUEVO USUARIO(CLIENTE)

@app.get("/register")
def mostrar_formulario_registro(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
    
@app.post("/register")
def register(usuario: Usuario):
    usuario_repo = UsuarioRepository()
    cliente_repo = ClienteRepository()

    # Verificar si el correo ya está registrado
    if usuario_repo.get_by_email(usuario.correo):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Asignar Tipo_idTipo como 2 (cliente)
    usuario.Tipo_idTipo = 2

    # Crear usuario
    id_usuario = usuario_repo.create(usuario)

    # Crear cliente vinculado
    nuevo_cliente = Cliente(n_dataloggers=0, Usuarios_idUsuarios=id_usuario)
    cliente_repo.create(nuevo_cliente)

    return {"mensaje": "Cuenta registrada exitosamente"}


# -------------------------------------------
# Dashboard Admin
# -------------------------------------------

@app.get("/admin/home/{nombre}")
def admin_home(nombre: str, request: Request):
    return templates.TemplateResponse("index-admin.html", {"request": request, "nombre": nombre})

@app.get("/{nombre}/admin/clientes")
async def mostrar_clientes(nombre: str,request: Request):
    cliente_repo = ClienteRepository()
    usuario_repo = UsuarioRepository()

    clientes = cliente_repo.get_all()
    clientes_completos = []

    for cliente in clientes:
        usuario = usuario_repo.get_by_id(cliente.Usuarios_idUsuarios)
        if usuario:
            clientes_completos.append({
                "idClientes": cliente.idClientes,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "n_dataloggers": cliente.n_dataloggers
            })

    return templates.TemplateResponse("clientes.html", {
        "request": request,
        "clientes": clientes_completos,
        "nombre": nombre
    })

@app.get("/{nombre}/admin/admin-dataloggers")
def ver_clientes_y_dataloggers(nombre: str, request: Request):
    usuario_repo = UsuarioRepository()
    cliente_repo = ClienteRepository()

    admin = usuario_repo.get_by_nombre(nombre)
    if not admin or admin.Tipo_idTipo != 1:
        raise HTTPException(status_code=403, detail="Acceso no autorizado.")

    clientes = cliente_repo.get_all()
    clientes_info = []

    for cliente in clientes:
        usuario = usuario_repo.get_by_id(cliente.Usuarios_idUsuarios)
        if usuario:
            clientes_info.append({
                "idClientes": cliente.idClientes,
                "nombre": usuario.nombre,
                "n_dataloggers": cliente.n_dataloggers
            })

    return templates.TemplateResponse("admin-dataloggers.html", {
        "request": request,
        "clientes": clientes_info,
        "nombre": nombre #correccion
    })

@app.get("/{nombre}/admin/asignar-datalogger/{cliente_id}")
async def mostrar_form_datalogger(nombre: str, cliente_id: int, request: Request):
    return templates.TemplateResponse("crear-datalogger.html", {
        "request": request,
        "cliente_id": cliente_id,
        "nombre": nombre  # se usa en el sidebar y redirect
    })

# -------------------------------------------
# Dashboard Cliente
# -------------------------------------------

@app.get("/home/{nombre}")
def home(nombre: str, request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nombre": nombre})

# -------------------------------------------
# Datalogers
# -------------------------------------------

# @app.get("/dataloggers/datos")
# async def mostrar_dataloggers(request: Request, service: DataloggerService = Depends(get_datalogger_service)):
#     dataloggers = service.get_all_dataloggers()
#     return templates.TemplateResponse("dataloggers.html", {
#         "request": request,
#         "dataloggers": dataloggers
#     })

@app.get("/{nombre}/dataloggers/datos")
async def mostrar_dataloggers(nombre: str, request: Request, service: DataloggerService = Depends(get_datalogger_service)):
    cliente_id = obtener_cliente_id_desde_nombre(nombre)
    dataloggers = [d for d in service.get_all_dataloggers() if d.Clientes_idClientes == cliente_id]
    return templates.TemplateResponse("dataloggers.html", {
        "request": request,
        "dataloggers": dataloggers,
        "nombre": nombre
    })


# @app.get("/dataloggers/crear")
# async def formulario_crear_datalogger(request: Request):
#     cliente_id = 1  # Simula el ID del cliente. Luego puedes sacarlo de sesión.
#     return templates.TemplateResponse("crear-datalogger.html", {
#         "request": request,
#         "cliente_id": cliente_id
#     })

@app.get("/{nombre}/dataloggers/crear")
async def formulario_crear_datalogger(nombre: str, request: Request):
    cliente_id = obtener_cliente_id_desde_nombre(nombre)
    return templates.TemplateResponse("crear-datalogger.html", {
        "request": request,
        "cliente_id": cliente_id,
        "nombre": nombre
    })

# -------------------------------------------
# Sensores
# -------------------------------------------

# @app.get("/sensores/datos")
# async def mostrar_sensores(request: Request, service: SensorService = Depends(get_sensor_service)):
#     sensores = service.get_all_sensors()
#     return templates.TemplateResponse("sensores.html", {
#         "request": request,
#         "sensores": sensores
#     })

@app.get("/{nombre}/sensores/datos")
async def mostrar_sensores(nombre: str, request: Request, sensor_service: SensorService = Depends(get_sensor_service), datalogger_service: DataloggerService = Depends(get_datalogger_service)):
    cliente_id = obtener_cliente_id_desde_nombre(nombre)
    dataloggers = [d for d in datalogger_service.get_all_dataloggers() if d.Clientes_idClientes == cliente_id]
    ids_dataloggers_cliente = [d.idDatalogger for d in dataloggers]
    sensores = [s for s in sensor_service.get_all_sensors() if s.Datalogger_idDatalogger in ids_dataloggers_cliente]
    return templates.TemplateResponse("sensores.html", {
        "request": request,
        "sensores": sensores,
        "nombre": nombre
    })


# @app.get("/sensores/crear")
# async def mostrar_formulario_sensor(request: Request, service: DataloggerService = Depends(get_datalogger_service)):
#     dataloggers = service.get_all_dataloggers()
#     return templates.TemplateResponse("crear-sensor.html", {
#         "request": request,
#         "dataloggers": dataloggers
#     })

@app.get("/{nombre}/sensores/crear")
async def mostrar_formulario_sensor(nombre: str, request: Request, service: DataloggerService = Depends(get_datalogger_service)):
    cliente_id = obtener_cliente_id_desde_nombre(nombre)
    dataloggers = [d for d in service.get_all_dataloggers() if d.Clientes_idClientes == cliente_id]
    return templates.TemplateResponse("crear-sensor.html", {
        "request": request,
        "dataloggers": dataloggers,
        "nombre": nombre
    })

# -------------------------------------------
# Mediciones
# -------------------------------------------

# @app.get("/mediciones/sensor/{id_sensor}")
# async def mostrar_mediciones_por_sensor(id_sensor: int, request: Request, service: MedicionService = Depends(get_medicion_service)):
#     mediciones = service.get_mediciones_by_sensor(id_sensor)
#     return templates.TemplateResponse("mediciones.html", {
#         "request": request,
#         "mediciones": mediciones,
#         "id_sensor": id_sensor
#     })

@app.get("/{nombre}/mediciones/sensor/{id_sensor}")
async def mostrar_mediciones_por_sensor(nombre: str, id_sensor: int, request: Request, service: MedicionService = Depends(get_medicion_service), sensor_service: SensorService = Depends(get_sensor_service), datalogger_service: DataloggerService = Depends(get_datalogger_service)):
    cliente_id = obtener_cliente_id_desde_nombre(nombre)
    
    sensor = sensor_service.get_sensor(id_sensor)
    datalogger = datalogger_service.get_datalogger(sensor.Datalogger_idDatalogger)

    if datalogger.Clientes_idClientes != cliente_id:
        raise HTTPException(status_code=403, detail="Acceso denegado a este sensor")

    mediciones = service.get_mediciones_by_sensor(id_sensor)
    return templates.TemplateResponse("mediciones.html", {
        "request": request,
        "mediciones": mediciones,
        "id_sensor": id_sensor,
        "nombre": nombre
    })


# -------------------------------------------
# Helpers
# -------------------------------------------

def obtener_cliente_id_desde_nombre(nombre: str) -> int:
    usuario_repo = UsuarioRepository()
    cliente_repo = ClienteRepository()
    
    usuario = usuario_repo.get_by_nombre(nombre)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cliente = cliente_repo.get_by_usuario_id(usuario.idUsuarios)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente.idClientes


# -------------------------------------------
# Ejecutar con Uvicorn
# -------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
