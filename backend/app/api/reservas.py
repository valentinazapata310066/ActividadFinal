from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta
from app.db import get_db
from app.models.reserva import Reserva
from app.models.espacio import Espacio
from app.schemas.reserva import ReservaCrear, ReservaRespuesta, ReservaActualizar
from app.services.auth_service import get_usuario_actual, get_admin_actual

router = APIRouter(prefix="/reservas", tags=["Reservas"])

def validar_reglas_negocio(datos: ReservaCrear, espacio: Espacio, db: Session):
    # Regla F — hora inicio < hora fin
    if datos.hora_inicio >= datos.hora_fin:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor a la hora de fin")

    # Regla D — mínimo 24 horas de anticipación
    fecha_hora_inicio = datetime.combine(datos.fecha, datos.hora_inicio)
    if fecha_hora_inicio < datetime.now() + timedelta(hours=24):
        raise HTTPException(status_code=400, detail="La reserva debe realizarse con al menos 24 horas de anticipación")

    # Regla E — horario permitido
    dia_semana = datos.fecha.weekday()
    if dia_semana == 6:
        raise HTTPException(status_code=400, detail="No se permiten reservas los domingos")

    hora_inicio_permitida = time(7, 0)
    hora_fin_permitida = time(20, 0)

    if dia_semana == 5:  # Sábado
        hora_inicio_permitida = time(8, 0)
        hora_fin_permitida = time(12, 0)

    if datos.hora_inicio < hora_inicio_permitida or datos.hora_fin > hora_fin_permitida:
        raise HTTPException(status_code=400, detail="Horario no permitido")

    # Regla G — no reservar espacios inactivos
    estados_bloqueados = ["inactivo", "en mantenimiento", "no disponible"]
    if espacio.estado in estados_bloqueados:
        raise HTTPException(status_code=400, detail=f"El espacio está {espacio.estado} y no puede reservarse")

    # Regla H — capacidad máxima
    if datos.cantidad_asistentes > espacio.capacidad:
        raise HTTPException(
            status_code=400,
            detail=f"La cantidad de asistentes supera la capacidad del espacio ({espacio.capacidad})"
        )

    # Regla C — no reservas superpuestas
    conflicto = db.query(Reserva).filter(
        Reserva.id_espacio == datos.id_espacio,
        Reserva.fecha == datos.fecha,
        Reserva.estado.in_(["esperando", "aprobada"]),
        Reserva.hora_inicio < datos.hora_fin,
        Reserva.hora_fin > datos.hora_inicio
    ).first()

    if conflicto:
        raise HTTPException(status_code=400, detail="El espacio ya tiene una reserva en ese horario")


@router.post("/", response_model=ReservaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    datos: ReservaCrear,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    espacio = db.query(Espacio).filter(Espacio.id_espacio == datos.id_espacio).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")

    validar_reglas_negocio(datos, espacio, db)

    nueva = Reserva(
        id_usuario=usuario_actual.id_usuario,
        id_espacio=datos.id_espacio,
        fecha=datos.fecha,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        cantidad_asistentes=datos.cantidad_asistentes,
        estado="esperando"
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[ReservaRespuesta])
def listar_reservas(
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    if usuario_actual.rol == "admin":
        return db.query(Reserva).all()
    return db.query(Reserva).filter(
        Reserva.id_usuario == usuario_actual.id_usuario
    ).all()

@router.get("/{id_reserva}", response_model=ReservaRespuesta)
def obtener_reserva(
    id_reserva: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
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
    reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    estados_validos = ["esperando", "aprobada", "rechazada"]
    if datos.estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Debe ser uno de: {estados_validos}")

    reserva.estado = datos.estado
    db.commit()
    db.refresh(reserva)
    return reserva

@router.delete("/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_reserva(
    id_reserva: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_usuario_actual)
):
    reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if usuario_actual.rol != "admin" and reserva.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=403, detail="No puedes cancelar esta reserva")

    if reserva.estado == "aprobada":
        raise HTTPException(status_code=400, detail="No puedes cancelar una reserva aprobada")

    db.delete(reserva)
    db.commit()