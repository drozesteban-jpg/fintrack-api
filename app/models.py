import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base

class TipoTransaccion(str, enum.Enum):
    ingreso = "ingreso"
    gasto = "gasto"

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(Enum(TipoTransaccion), nullable=False)
    categoria = Column(String, nullable=False)
    fecha = Column(DateTime, server_default=func.now())