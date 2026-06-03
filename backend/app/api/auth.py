from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.usuarios import Usuarios
from app.services.auth_service import verificar_password, crear_token
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuarios = db.query(Usuarios).filter(
        Usuarios.correo == form_data.username
    ).first()

    if not usuarios or not verificar_password(form_data.password, usuarios.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    if not usuarios.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuarios inactivo"
        )

    token = crear_token({
        "sub": usuarios.correo,
        "id_usuario": usuarios.id_usuarios,
        "rol": usuarios.rol
    })

    return {"access_token": token, "token_type": "bearer"}