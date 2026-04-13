from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter()


@router.post("/transacciones", response_model=schemas.TransaccionResponse)
def crear_transaccion(
    transaccion: schemas.TransaccionCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    nueva = models.Transaccion(**transaccion.model_dump(), user_id=current_user.id)
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
    current_user: models.Usuario = Depends(get_current_user),
):
    q = db.query(models.Transaccion).filter(models.Transaccion.user_id == current_user.id)
    if tipo is not None:
        q = q.filter(models.Transaccion.tipo == tipo)
    if categoria is not None:
        q = q.filter(models.Transaccion.categoria == categoria)
    return q.offset(skip).limit(limit).all()


@router.get("/transacciones/{id}", response_model=schemas.TransaccionResponse)
def obtener_transaccion(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    transaccion = (
        db.query(models.Transaccion)
        .filter(models.Transaccion.id == id, models.Transaccion.user_id == current_user.id)
        .first()
    )
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.delete("/transacciones/{id}")
def eliminar_transaccion(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    transaccion = (
        db.query(models.Transaccion)
        .filter(models.Transaccion.id == id, models.Transaccion.user_id == current_user.id)
        .first()
    )
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    db.delete(transaccion)
    db.commit()
    return {"mensaje": "Transacción eliminada correctamente"}


@router.get("/resumen")
def resumen(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    rows = (
        db.query(models.Transaccion.tipo, func.sum(models.Transaccion.monto))
        .filter(models.Transaccion.user_id == current_user.id)
        .group_by(models.Transaccion.tipo)
        .all()
    )
    totales = {tipo: total for tipo, total in rows}
    ingresos = totales.get(models.TipoTransaccion.ingreso, 0.0)
    gastos = totales.get(models.TipoTransaccion.gasto, 0.0)
    return {
        "ingresos_totales": ingresos,
        "gastos_totales": gastos,
        "balance": ingresos - gastos,
    }
