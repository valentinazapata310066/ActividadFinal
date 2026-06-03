from sqlalchemy.orm import Session
from app.models.reserva import Reserva
from app.models.espacio import Espacio
from app.schemas.reserva import ReservaCrear
from fastapi import HTTPException

def crear(db: Session, datos: ReservaCrear, id_usuario: int):
    # Validar que el espacio existe y está disponible
    espacio = db.query(Espacio).filter(Espacio.id_espacio == datos.id_espacio).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    if espacio.estado != "disponible":
        raise HTTPException(status_code=400, detail="El espacio no está disponible")
    
    # Validar capacidad
    if datos.cantidad_asistentes > espacio.capacidad:
        raise HTTPException(
            status_code=400, 
            detail=f"La capacidad máxima del espacio es {espacio.capacidad} personas"
        )
    
    # Validar horario permitido
    dia_semana = datos.fecha.weekday()
    hora = datos.hora_inicio
    
    if dia_semana == 6:
        raise HTTPException(
            status_code=400, 
            detail="No se permiten reservas los domingos"
        )
    elif dia_semana == 5:
        if hora.hour < 8 or hora.hour >= 12:
            raise HTTPException(
                status_code=400, 
                detail="Los sábados solo se permiten reservas de 8:00 a 12:00"
            )
    else:
        if hora.hour < 7 or hora.hour >= 20:
            raise HTTPException(
                status_code=400, 
                detail="De lunes a viernes solo se permiten reservas de 7:00 a 20:00"
            )
    
    # Validar no superposición
    reserva_existente = db.query(Reserva).filter(
        Reserva.id_espacio == datos.id_espacio,
        Reserva.fecha == datos.fecha,
        Reserva.estado.in_(["esperando", "aprobada"]),
        ((Reserva.hora_inicio < datos.hora_fin) & (Reserva.hora_fin > datos.hora_inicio))
    ).first()
    
    if reserva_existente:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe una reserva en ese horario"
        )
    
    nueva_reserva = Reserva(
        id_usuario=id_usuario,
        id_espacio=datos.id_espacio,
        fecha=datos.fecha,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        cantidad_asistentes=datos.cantidad_asistentes,
        estado="esperando"
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

def listar_todas(db: Session):
    return db.query(Reserva).all()

def listar_por_usuario(db: Session, id_usuario: int):
    return db.query(Reserva).filter(Reserva.id_usuario == id_usuario).all()

def listar_pendientes(db: Session):
    return db.query(Reserva).filter(Reserva.estado == "esperando").all()

def obtener_por_id(db: Session, id_reserva: int):
    return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

def actualizar_estado(db: Session, id_reserva: int, nuevo_estado: str):
    reserva = obtener_por_id(db, id_reserva)
    if not reserva:
        return None
    reserva.estado = nuevo_estado
    db.commit()
    db.refresh(reserva)
    return reserva

def eliminar(db: Session, id_reserva: int):
    reserva = obtener_por_id(db, id_reserva)
    if not reserva:
        return None
    db.delete(reserva)
    db.commit()
    return reserva