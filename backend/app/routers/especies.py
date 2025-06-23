from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import require_roles

router = APIRouter()

@router.get("/", response_model=List[schemas.EspecieResponse], summary="Listar especies")
def listar_especies(db: Session = Depends(get_db)):
    return db.query(models.Especie).filter(models.Especie.estado == True).all()

@router.post("/", response_model=schemas.EspecieResponse, summary="Crear especie")
def crear_especie(especie: schemas.EspecieCreate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    nueva = models.Especie(nombre=especie.nombre, estado=True)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id_especie}", response_model=schemas.EspecieResponse, summary="Actualizar especie")
def actualizar_especie(id_especie: int, datos: schemas.EspecieUpdate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    especie = db.query(models.Especie).filter(models.Especie.id_especie == id_especie, models.Especie.estado == True).first()
    if not especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(especie, campo, valor)
    db.commit()
    db.refresh(especie)
    return especie

@router.delete("/{id_especie}", summary="Eliminar especie lógicamente")
def eliminar_especie(id_especie: int, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    especie = db.query(models.Especie).filter(models.Especie.id_especie == id_especie, models.Especie.estado == True).first()
    if not especie:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    especie.estado = False
    db.commit()
    return {"mensaje": "Especie eliminada lógicamente"}