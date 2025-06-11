from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import require_roles

router = APIRouter()

# Listar todas las mascotas (público)
@router.get("/", response_model=List[schemas.MascotaResponse], summary="Listar todas las mascotas")
def listar_mascotas(db: Session = Depends(get_db)):
    mascotas = db.query(models.Mascota).filter(models.Mascota.estado == True).all()
    return mascotas

# Ver detalles de una mascota (público)
@router.get("/{id_mascota}", response_model=schemas.MascotaResponse, summary="Obtener detalles de una mascota")
def obtener_mascota(id_mascota: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id_mascota == id_mascota, models.Mascota.estado == True).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

# Registrar una mascota (solo voluntario o admin)
@router.post("/", response_model=schemas.MascotaResponse, summary="Registrar una nueva mascota")
def registrar_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    nueva_mascota = models.Mascota(
        nombre_mascota=mascota.nombre_mascota,
        sexo=mascota.sexo,
        id_especie=mascota.especie_id,
        id_raza=mascota.raza_id,
        edad=mascota.edad,
        estado_mascota=mascota.estado_mascota,
        descripcion=mascota.descripcion,
        estado=True,
        registrado_por=user["id_usuario"]
    )
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

# Actualizar una mascota (solo voluntario o admin)
@router.put("/{id_mascota}", response_model=schemas.MascotaResponse, summary="Actualizar datos de una mascota")
def actualizar_mascota(id_mascota: int, datos: schemas.MascotaUpdate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    mascota = db.query(models.Mascota).filter(models.Mascota.id_mascota == id_mascota, models.Mascota.estado == True).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(mascota, campo, valor)
    db.commit()
    db.refresh(mascota)
    return mascota

# Eliminación lógica de una mascota (solo voluntario o admin)
@router.delete("/{id_mascota}", summary="Eliminar mascota lógicamente")
def eliminar_mascota(id_mascota: int, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    mascota = db.query(models.Mascota).filter(models.Mascota.id_mascota == id_mascota, models.Mascota.estado == True).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    mascota.estado = False
    db.commit()
    return {"mensaje": "Mascota eliminada lógicamente"}

# Agregar foto a una mascota
@router.post("/{id_mascota}/fotos", response_model=schemas.FotoMascotaResponse, summary="Agregar foto a una mascota")
def agregar_foto_mascota(id_mascota: int, foto: schemas.FotoMascotaCreate, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    nueva_foto = models.FotoMascota(
        id_mascota=id_mascota,
        url=foto.url,
        descripcion=foto.descripcion,
        estado=True
    )
    db.add(nueva_foto)
    db.commit()
    db.refresh(nueva_foto)
    return nueva_foto

# Eliminar foto de mascota (lógica)
@router.delete("/fotos/{id_foto}", summary="Eliminar foto de mascota")
def eliminar_foto(id_foto: int, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    foto = db.query(models.FotoMascota).filter(models.FotoMascota.id_foto == id_foto, models.FotoMascota.estado == True).first()
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    foto.estado = False
    db.commit()
    return {"mensaje": "Foto eliminada lógicamente"}