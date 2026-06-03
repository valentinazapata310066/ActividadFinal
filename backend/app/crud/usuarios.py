from sqlalchemy.orm import Session
from app.models.usuarios import Usuarios
from app.schemas.usuarios import UsuarioCrear
from app.services.auth_service import hashear_password

def obtener_por_correo(db: Session, correo: str):
    return db.query(Usuarios).filter(Usuarios.correo == correo).first()

def obtener_por_id(db: Session, id_usuario: int):
    return db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()

def listar(db: Session):
    return db.query(Usuarios).all()

def crear(db: Session, datos: UsuarioCrear):
    nuevo = Usuarios(
        nombre=datos.nombre,
        correo=datos.correo,
        password_hash=hashear_password(datos.password),
        rol=datos.rol,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar(db: Session, id_usuario: int, datos):
    usuario = obtener_por_id(db, id_usuario)
    if not usuario:
        return None
    if datos.nombre: usuario.nombre = datos.nombre
    if datos.correo: usuario.correo = datos.correo
    if datos.rol: usuario.rol = datos.rol
    if datos.activo is not None: usuario.activo = datos.activo
    db.commit()
    db.refresh(usuario)
    return usuario