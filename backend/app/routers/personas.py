from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import crear_token
from ..auth.dependencies import get_current_user, require_roles

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/persona/{id_usuario}", summary="Obtener datos de persona por usuario")
def obtener_persona(id_usuario: int, db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    persona = db.query(models.Persona).filter(models.Persona.id_usuario == id_usuario, models.Persona.estado == True).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.get("/personas", summary="Listar personas")
def listar_personas(db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    personas = db.query(models.Persona).filter(models.Persona.estado == True).all()
    resultado = []
    for p in personas:
        resultado.append({
            "id_persona": p.id_persona,
            "id_usuario": p.id_usuario,
            "nombre": p.nombre,
            "apellido": p.apellido,
            "dni": p.dni,
            "telefono": p.telefono,
            "direccion": p.direccion,
            "estado": p.estado
        })
    return resultado

# Cambiar nombre
@router.put("/cambiar-nombre", summary="Cambiar nombre de la persona")
def cambiar_nombre(datos: schemas.CambiarNombre, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not usuario.persona:
        raise HTTPException(status_code=404, detail="Usuario o persona no encontrado")
    usuario.persona.nombre = datos.nuevo_nombre
    db.commit()
    return {"mensaje": "Nombre actualizado correctamente"}

# Cambiar apellido
@router.put("/cambiar-apellido", summary="Cambiar apellido de la persona")
def cambiar_apellido(datos: schemas.CambiarApellido, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not usuario.persona:
        raise HTTPException(status_code=404, detail="Usuario o persona no encontrado")
    usuario.persona.apellido = datos.nuevo_apellido
    db.commit()
    return {"mensaje": "Apellido actualizado correctamente"}

@router.put("/cambiar-dni", summary="Cambiar DNI de la persona")
def cambiar_dni(datos: schemas.CambiarDNI, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not usuario.persona:
        raise HTTPException(status_code=404, detail="Usuario o persona no encontrado")
    # Verifica si el DNI ya existe
    if db.query(models.Persona).filter(models.Persona.dni == datos.nuevo_dni).first():
        raise HTTPException(status_code=400, detail="El DNI ya existe")
    usuario.persona.dni = datos.nuevo_dni
    db.commit()
    return {"mensaje": "DNI actualizado correctamente"}

# Cambiar teléfono
@router.put("/cambiar-telefono", summary="Cambiar teléfono de la persona")
def cambiar_telefono(datos: schemas.CambiarTelefono, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not usuario.persona:
        raise HTTPException(status_code=404, detail="Usuario o persona no encontrado")
    usuario.persona.telefono = datos.nuevo_telefono
    db.commit()
    return {"mensaje": "Teléfono actualizado correctamente"}

# Cambiar dirección
@router.put("/cambiar-direccion", summary="Cambiar dirección de la persona")
def cambiar_direccion(datos: schemas.CambiarDireccion, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not usuario.persona:
        raise HTTPException(status_code=404, detail="Usuario o persona no encontrado")
    usuario.persona.direccion = datos.nueva_direccion
    db.commit()
    return {"mensaje": "Dirección actualizada correctamente"}


@router.delete("/persona/{id_persona}", summary="Eliminar persona lógicamente")
def eliminar_persona(id_persona: int, db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    persona = db.query(models.Persona).filter(models.Persona.id_persona == id_persona, models.Persona.estado == True).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    persona.estado = False
    # Elimina lógicamente los perfiles de adopción asociados
    for perfil in persona.perfiles_adopcion:
        perfil.estado = False
    db.commit()
    return {"mensaje": "Persona y perfiles de adopción eliminados lógicamente"}