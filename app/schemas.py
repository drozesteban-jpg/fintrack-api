from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from app.models import TipoTransaccion


class TransaccionBase(BaseModel):
    descripcion: str
    monto: float
    tipo: TipoTransaccion
    categoria: str


class TransaccionCreate(TransaccionBase):
    @field_validator("monto")
    @classmethod
    def validar_monto(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v


class TransaccionResponse(TransaccionBase):
    id: int
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str


class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
