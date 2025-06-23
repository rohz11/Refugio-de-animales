from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import require_roles

router = APIRouter()

@router.get("/", response_model=List[schemas.RazaResponse], summary="Listar razas")
def listar_razas(id_especie: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Raza).filter(models.Raza.estado == True)
    if id_especie:
        query = query.filter(models.Raza.id_especie == id_especie)
    return query.all()

@router.post("/", response_model=schemas.RazaResponse, summary="Crear raza")
def crear_raza(raza: schemas.RazaCreate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    nueva = models.Raza(nombre=raza.nombre, id_especie=raza.id_especie, estado=True)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id_raza}", response_model=schemas.RazaResponse, summary="Actualizar raza")
def actualizar_raza(id_raza: int, datos: schemas.RazaUpdate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    raza = db.query(models.Raza).filter(models.Raza.id_raza == id_raza, models.Raza.estado == True).first()
    if not raza:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(raza, campo, valor)
    db.commit()
    db.refresh(raza)
    return raza

@router.delete("/{id_raza}", summary="Eliminar raza lógicamente")
def eliminar_raza(id_raza: int, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    raza = db.query(models.Raza).filter(models.Raza.id_raza == id_raza, models.Raza.estado == True).first()
    if not raza:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    raza.estado = False
    db.commit()
    return {"mensaje": "Raza eliminada lógicamente"}