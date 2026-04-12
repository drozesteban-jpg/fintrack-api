from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/transacciones", response_model=schemas.TransaccionResponse)
def crear_transaccion(transaccion: schemas.TransaccionCreate, db: Session = Depends(get_db)):
    nueva = models.Transaccion(**transaccion.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/transacciones", response_model=List[schemas.TransaccionResponse])
def listar_transacciones(db: Session = Depends(get_db)):
    return db.query(models.Transaccion).all()

@router.get("/transacciones/{id}", response_model=schemas.TransaccionResponse)
def obtener_transaccion(id: int, db: Session = Depends(get_db)):
    transaccion = db.query(models.Transaccion).filter(models.Transaccion.id == id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion

@router.delete("/transacciones/{id}")
def eliminar_transaccion(id: int, db: Session = Depends(get_db)):
    transaccion = db.query(models.Transaccion).filter(models.Transaccion.id == id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    db.delete(transaccion)
    db.commit()
    return {"mensaje": "Transacción eliminada correctamente"}

@router.get("/resumen")
def resumen(db: Session = Depends(get_db)):
    transacciones = db.query(models.Transaccion).all()
    ingresos = sum(t.monto for t in transacciones if t.tipo == "ingreso")
    gastos = sum(t.monto for t in transacciones if t.tipo == "gasto")
    balance = ingresos - gastos
    return {
        "ingresos_totales": ingresos,
        "gastos_totales": gastos,
        "balance": balance
    }