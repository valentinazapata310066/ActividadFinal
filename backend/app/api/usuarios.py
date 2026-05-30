from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta, UsuarioActualizar
from app.services.auth_service import hashear_password, get_usuario_actual, get_admin_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    datos: UsuarioCrear,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    existente = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo = Usuario(
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

@router.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registro_publico(datos: UsuarioCrear, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        password_hash=hashear_password(datos.password),
        rol="usuario",
        activo=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios(
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    return db.query(Usuario).all()

@router.get("/me", response_model=UsuarioRespuesta)
def obtener_perfil(usuario_actual=Depends(get_usuario_actual)):
    return usuario_actual

@router.get("/{id_usuario}", response_model=UsuarioRespuesta)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/{id_usuario}", response_model=UsuarioRespuesta)
def actualizar_usuario(
    id_usuario: int,
    datos: UsuarioActualizar,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.nombre: usuario.nombre = datos.nombre
    if datos.correo: usuario.correo = datos.correo
    if datos.rol: usuario.rol = datos.rol
    if datos.activo is not None: usuario.activo = datos.activo

    db.commit()
    db.refresh(usuario)
    return usuario