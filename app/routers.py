from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
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
def listar_transacciones(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    tipo: Optional[models.TipoTransaccion] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Transaccion)
    if tipo is not None:
        q = q.filter(models.Transaccion.tipo == tipo)
    if categoria is not None:
        q = q.filter(models.Transaccion.categoria == categoria)
    return q.offset(skip).limit(limit).all()

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