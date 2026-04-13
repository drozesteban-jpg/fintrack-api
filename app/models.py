import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class TipoTransaccion(str, enum.Enum):
    ingreso = "ingreso"
    gasto = "gasto"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transacciones = relationship("Transaccion", back_populates="usuario")


class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(Enum(TipoTransaccion), nullable=False)
    categoria = Column(String, nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="transacciones")
