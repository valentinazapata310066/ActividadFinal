from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.reserva import ReservaCrear, ReservaRespuesta, ReservaActualizar
from app.services.auth_service import get_usuario_actual, get_admin_actual
from app.crud import reserva as crud_reserva

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/", response_model=ReservaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    datos: ReservaCrear,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    return crud_reserva.crear(db, datos, usuario_actual.id_usuario)

@router.get("/", response_model=list[ReservaRespuesta])
def listar_reservas(
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    if usuario_actual.rol == "admin":
        return crud_reserva.listar(db)
    return crud_reserva.listar_por_usuario(db, usuario_actual.id_usuario)

@router.get("/{id_reserva}", response_model=ReservaRespuesta)
def obtener_reserva(
    id_reserva: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    reserva = crud_reserva.obtener_por_id(db, id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if usuario_actual.rol != "admin" and reserva.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta reserva")
    return reserva

@router.patch("/{id_reserva}/estado", response_model=ReservaRespuesta)
def actualizar_estado(
    id_reserva: int,
    datos: ReservaActualizar,
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    reserva = crud_reserva.actualizar_estado(db, id_reserva, datos.estado)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.delete("/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_reserva(
    id_reserva: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    reserva = crud_reserva.obtener_por_id(db, id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if usuario_actual.rol != "admin" and reserva.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=403, detail="No puedes cancelar esta reserva")
    if reserva.estado == "aprobada":
        raise HTTPException(status_code=400, detail="No puedes cancelar una reserva aprobada")
    crud_reserva.eliminar(db, id_reserva)