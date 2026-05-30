from pydantic import BaseModel

class Login(BaseModel):
    correo: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    correo: str
    rol: str
    id_usuario: int