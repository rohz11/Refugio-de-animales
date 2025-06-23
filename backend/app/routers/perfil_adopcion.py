from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import require_roles

router = APIRouter()

# Crear perfil de adopción (solo si no existe)
@router.post("/", response_model=schemas.PerfilAdopcionResponse, summary="Crear perfil de adopción")
def crear_perfil(perfil: schemas.PerfilAdopcionCreate, db: Session = Depends(get_db), user=Depends(require_roles(["Usuario"]))):
    persona = db.query(models.Persona).filter(models.Persona.id_usuario == user["id_usuario"]).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    existente = db.query(models.PerfilAdopcion).filter(
        models.PerfilAdopcion.id_persona == persona.id_persona,
        models.PerfilAdopcion.estado == True
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya tienes un perfil de adopción")
    nuevo_perfil = models.PerfilAdopcion(
        id_persona=persona.id_persona,
        nombre=perfil.nombre,
        direccion=perfil.direccion,
        telefono=perfil.telefono,
        informacion_adicional=perfil.informacion_adicional,
        estado=True
    )
    db.add(nuevo_perfil)
    db.commit()
    db.refresh(nuevo_perfil)
    return nuevo_perfil

# Ver mi perfil de adopción (usuario)
@router.get("/mi-perfil", response_model=schemas.PerfilAdopcionResponse, summary="Ver mi perfil de adopción")
def ver_mi_perfil(db: Session = Depends(get_db), user=Depends(require_roles(["Usuario"]))):
    persona = db.query(models.Persona).filter(models.Persona.id_usuario == user["id_usuario"]).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    perfil = db.query(models.PerfilAdopcion).filter(
        models.PerfilAdopcion.id_persona == persona.id_persona,
        models.PerfilAdopcion.estado == True
    ).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

# Actualizar mi perfil de adopción (usuario)
@router.put("/mi-perfil", response_model=schemas.PerfilAdopcionResponse, summary="Actualizar mi perfil de adopción")
def actualizar_mi_perfil(datos: schemas.PerfilAdopcionUpdate, db: Session = Depends(get_db), user=Depends(require_roles(["Usuario"]))):
    persona = db.query(models.Persona).filter(models.Persona.id_usuario == user["id_usuario"]).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    perfil = db.query(models.PerfilAdopcion).filter(
        models.PerfilAdopcion.id_persona == persona.id_persona,
        models.PerfilAdopcion.estado == True
    ).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(perfil, campo, valor)
    db.commit()
    db.refresh(perfil)
    return perfil

# Eliminar mi perfil de adopción (lógica, usuario)
@router.delete("/mi-perfil", summary="Eliminar mi perfil de adopción lógicamente")
def eliminar_mi_perfil(db: Session = Depends(get_db), user=Depends(require_roles(["Usuario"]))):
    persona = db.query(models.Persona).filter(models.Persona.id_usuario == user["id_usuario"]).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    perfil = db.query(models.PerfilAdopcion).filter(
        models.PerfilAdopcion.id_persona == persona.id_persona,
        models.PerfilAdopcion.estado == True
    ).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    perfil.estado = False
    db.commit()
    return {"mensaje": "Perfil eliminado lógicamente"}

# Ver perfil de adopción por ID (voluntario/admin)
@router.get("/{id_perfil}", response_model=schemas.PerfilAdopcionResponse, summary="Ver perfil de adopción por ID")
def ver_perfil_id(id_perfil: int, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    perfil = db.query(models.PerfilAdopcion).filter(
        models.PerfilAdopcion.id_perfil == id_perfil,
        models.PerfilAdopcion.estado == True
    ).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

# Listar todos los perfiles de adopción (voluntario/admin)
@router.get("/", response_model=List[schemas.PerfilAdopcionResponse], summary="Listar todos los perfiles de adopción")
def listar_perfiles(db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    perfiles = db.query(models.PerfilAdopcion).filter(models.PerfilAdopcion.estado == True).all()
    return perfiles