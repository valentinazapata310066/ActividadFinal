from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.usuarios import UsuarioCrear, UsuarioRespuesta, UsuarioActualizar
from app.services.auth_service import get_usuario_actual, get_admin_actual
from app.crud import usuarios as crud_usuario

router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.post("/", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    datos: UsuarioCrear,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    existente = crud_usuario.obtener_por_correo(db, datos.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return crud_usuario.crear(db, datos)

@router.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registro_publico(datos: UsuarioCrear, db: Session = Depends(get_db)):
    existente = crud_usuario.obtener_por_correo(db, datos.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    datos.rol = "usuario"
    return crud_usuario.crear(db, datos)

@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuario(
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    return crud_usuario.listar(db)

@router.get("/me", response_model=UsuarioRespuesta)
def obtener_perfil(usuario_actual=Depends(get_usuario_actual)):
    return usuario_actual

@router.get("/{id_usuario}", response_model=UsuarioRespuesta)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    usuario = crud_usuario.obtener_por_id(db, id_usuario)
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
    usuario = crud_usuario.actualizar(db, id_usuario, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario