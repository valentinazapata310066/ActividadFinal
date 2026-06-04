from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.espacio import EspacioCrear, EspacioRespuesta, EspacioActualizar
from app.services.auth_service import get_usuario_actual, get_admin_actual
from app.crud import espacio as crud_espacio

router = APIRouter(prefix="/espacios", tags=["Espacios"])

@router.post("/", response_model=EspacioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_espacio(
    datos: EspacioCrear,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    return crud_espacio.crear(db, datos)

@router.get("/", response_model=list[EspacioRespuesta])
def listar_espacios(
    db: Session = Depends(get_db),
    _=Depends(get_usuario_actual)
):
    return crud_espacio.listar(db)

@router.get("/disponibles", response_model=list[EspacioRespuesta])
def listar_espacios_disponibles(
    db: Session = Depends(get_db),
    _=Depends(get_usuario_actual)
):
    return crud_espacio.listar_disponibles(db)

@router.get("/{id_espacio}", response_model=EspacioRespuesta)
def obtener_espacio(
    id_espacio: int,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_actual)
):
    espacio = crud_espacio.obtener_por_id(db, id_espacio)
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
    espacio = crud_espacio.actualizar(db, id_espacio, datos)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return espacio

@router.delete("/{id_espacio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_espacio(
    id_espacio: int,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    espacio = crud_espacio.eliminar(db, id_espacio)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")