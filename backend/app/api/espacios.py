from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.espacio import Espacio
from app.schemas.espacio import EspacioCrear, EspacioRespuesta, EspacioActualizar
from app.services.auth_service import get_usuario_actual, get_admin_actual

router = APIRouter(prefix="/espacios", tags=["Espacios"])

@router.post("/", response_model=EspacioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_espacio(
    datos: EspacioCrear,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    nuevo = Espacio(
        nombre=datos.nombre,
        ubicacion=datos.ubicacion,
        capacidad=datos.capacidad,
        estado=datos.estado
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[EspacioRespuesta])
def listar_espacios(
    db: Session = Depends(get_db),
    _=Depends(get_usuario_actual)
):
    return db.query(Espacio).all()

@router.get("/{id_espacio}", response_model=EspacioRespuesta)
def obtener_espacio(
    id_espacio: int,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_actual)
):
    espacio = db.query(Espacio).filter(Espacio.id_espacio == id_espacio).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return espacio

@router.patch("/{id_espacio}", response_model=EspacioRespuesta)
def actualizar_espacio(
    id_espacio: int,
    datos: EspacioActualizar,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    espacio = db.query(Espacio).filter(Espacio.id_espacio == id_espacio).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")

    if datos.nombre: espacio.nombre = datos.nombre
    if datos.ubicacion: espacio.ubicacion = datos.ubicacion
    if datos.capacidad: espacio.capacidad = datos.capacidad
    if datos.estado: espacio.estado = datos.estado

    db.commit()
    db.refresh(espacio)
    return espacio

@router.delete("/{id_espacio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_espacio(
    id_espacio: int,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    espacio = db.query(Espacio).filter(Espacio.id_espacio == id_espacio).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    db.delete(espacio)
    db.commit()