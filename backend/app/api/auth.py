from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.usuario import Usuario
from app.services.auth_service import verificar_password, crear_token
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.correo == form_data.username
    ).first()

    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    token = crear_token({
        "sub": usuario.correo,
        "id_usuario": usuario.id_usuario,
        "rol": usuario.rol
    })

    return {"access_token": token, "token_type": "bearer"}