from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import require_roles, get_current_user

router = APIRouter()

# 1. Solicitar adopción (usuario)
@router.post("/", response_model=schemas.AdopcionResponse, summary="Solicitar adopción de una mascota")
def solicitar_adopcion(datos: schemas.AdopcionCreate, db: Session = Depends(get_db), user=Depends(require_roles(["Usuario"]))):
    # Verifica que la mascota y el perfil existan y estén activos
    mascota = db.query(models.Mascota).filter(models.Mascota.id_mascota == datos.id_mascota, models.Mascota.estado == True).first()
    perfil = db.query(models.PerfilAdopcion).filter(models.PerfilAdopcion.id_perfil == datos.id_perfil, models.PerfilAdopcion.estado == True).first()
    if not mascota or not perfil:
        raise HTTPException(status_code=404, detail="Mascota o perfil no encontrado")
    # Verifica que el usuario sea dueño del perfil
    persona = perfil.persona
    if not persona or persona.id_usuario != user["id_usuario"]:
        raise HTTPException(status_code=403, detail="No puedes usar este perfil")
    # Crea la solicitud
    nueva_adopcion = models.Adopcion(
        id_perfil=datos.id_perfil,
        id_mascota=datos.id_mascota,
        id_usuario=user["id_usuario"],
        estado_adopcion="Pendiente",
        estado=True
    )
    db.add(nueva_adopcion)
    db.commit()
    db.refresh(nueva_adopcion)
    return nueva_adopcion

# 2. Ver solicitudes propias (usuario)
@router.get("/mis-solicitudes", response_model=List[schemas.AdopcionResponse], summary="Ver mis solicitudes de adopción")
def mis_solicitudes(db: Session = Depends(get_db), user=Depends(require_roles(["Usuario"]))):
    solicitudes = db.query(models.Adopcion).filter(models.Adopcion.id_usuario == user["id_usuario"], models.Adopcion.estado == True).all()
    return solicitudes

# 3. Listar todas las solicitudes (voluntario/admin)
@router.get("/", response_model=List[schemas.AdopcionResponse], summary="Listar todas las solicitudes de adopción")
def listar_solicitudes(db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    solicitudes = db.query(models.Adopcion).filter(models.Adopcion.estado == True).all()
    return solicitudes

# 4. Asignar entrevista (voluntario/admin)
@router.put("/{id_adopcion}/asignar-entrevista", response_model=schemas.AdopcionResponse, summary="Asignar entrevistador y fecha")
def asignar_entrevista(id_adopcion: int, datos: schemas.AsignarEntrevista, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    adopcion = db.query(models.Adopcion).filter(models.Adopcion.id_adopcion == id_adopcion, models.Adopcion.estado == True).first()
    if not adopcion:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    # Verifica que el entrevistador exista y sea voluntario/admin
    entrevistador = db.query(models.Usuario).filter(models.Usuario.id_usuario == datos.id_entrevistador, models.Usuario.estado == True).first()
    if not entrevistador:
        raise HTTPException(status_code=404, detail="Entrevistador no encontrado")
    adopcion.fecha_entrevista = datos.fecha_entrevista
    adopcion.id_entrevistador = datos.id_entrevistador
    db.commit()
    db.refresh(adopcion)
    return adopcion

# 5. Cambiar estado de la solicitud (voluntario/admin)
@router.put("/{id_adopcion}/cambiar-estado", response_model=schemas.AdopcionResponse, summary="Cambiar estado de la solicitud")
def cambiar_estado(id_adopcion: int, datos: schemas.CambiarEstadoAdopcion, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    adopcion = db.query(models.Adopcion).filter(models.Adopcion.id_adopcion == id_adopcion, models.Adopcion.estado == True).first()
    if not adopcion:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    adopcion.estado_adopcion = datos.estado_adopcion
    adopcion.respuesta = datos.respuesta
    db.commit()
    db.refresh(adopcion)
    return adopcion

# 6. Eliminación lógica de una solicitud (voluntario/admin)
@router.delete("/{id_adopcion}", summary="Eliminar solicitud de adopción lógicamente")
def eliminar_adopcion(id_adopcion: int, db: Session = Depends(get_db), user=Depends(require_roles(["Voluntario", "Administrador"]))):
    adopcion = db.query(models.Adopcion).filter(models.Adopcion.id_adopcion == id_adopcion, models.Adopcion.estado == True).first()
    if not adopcion:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    adopcion.estado = False
    db.commit()
    return {"mensaje": "Solicitud eliminada lógicamente"}