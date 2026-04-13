from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime

class TransaccionBase(BaseModel):
    descripcion: str
    monto: float
    tipo: str
    categoria: str

class TransaccionCreate(TransaccionBase):
    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, v):
        if v not in ["ingreso", "gasto"]:
            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'")
        return v

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