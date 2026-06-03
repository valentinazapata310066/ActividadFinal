from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta  # ← AGREGAR ESTO
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
    # ✅ AGREGAR ESTA VALIDACIÓN
    fecha_hora_reserva = datetime.combine(datos.fecha, datos.hora_inicio)
    if fecha_hora_reserva < datetime.now() + timedelta(hours=24):
        raise HTTPException(
            status_code=400, 
            detail="La reserva debe hacerse con al menos 24 horas de anticipación"
        )
    
    return crud_reserva.crear(db, datos, usuario_actual.id_usuario)

# ✅ AGREGAR ESTOS DOS ENDPOINTS
@router.get("/mis-reservas", response_model=list[ReservaRespuesta])
def mis_reservas(
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    return crud_reserva.listar_por_usuario(db, usuario_actual.id_usuario)

@router.get("/pendientes", response_model=list[ReservaRespuesta])
def reservas_pendientes(
    db: Session = Depends(get_db),
    _=Depends(get_admin_actual)
):
    return crud_reserva.listar_pendientes(db)

# El resto de tu código sigue igual
@router.get("/", response_model=list[ReservaRespuesta])
def listar_reservas(
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    if usuario_actual.rol == "admin":
        return crud_reserva.listar_todas(db)
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
    if datos.estado not in ["aprobada", "rechazada"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
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
    return None