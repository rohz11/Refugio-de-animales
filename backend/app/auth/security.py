from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import crear_token
from ..auth.dependencies import get_current_user, require_roles

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ruta para registrar un nuevo usuario
@router.post("/registro", summary="Registrar un nuevo usuario")
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica si el alias o correo ya existen
    db_usuario = db.query(models.Usuario).filter(
        (models.Usuario.alias == usuario.alias) | (models.Usuario.correo == usuario.correo),
        models.Usuario.estado == True
    ).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El alias o correo ya existe")

    db_dni = db.query(models.Persona).filter(
        models.Persona.dni == usuario.persona.dni,
        models.Persona.estado == True
    ).first()
    if db_dni:
        raise HTTPException(status_code=400, detail="El DNI ya existe")
    
    # 1. Crea el usuario primero
    hashed_password = pwd_context.hash(usuario.clave)
    nuevo_usuario = models.Usuario(
        alias=usuario.alias,
        clave=hashed_password,
        correo=usuario.correo,
        pregunta_seguridad=usuario.pregunta_seguridad,
        respuesta_seguridad=usuario.respuesta_seguridad,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # 2. Crea la persona asociada a ese usuario (sin correo)
    persona = models.Persona(
        id_usuario=nuevo_usuario.id_usuario,
        nombre=usuario.persona.nombre,
        apellido=usuario.persona.apellido,
        dni=usuario.persona.dni,
        telefono=usuario.persona.telefono,
        direccion=usuario.persona.direccion,
        estado=True
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)

    # Asigna un rol por defecto (por ejemplo, id_rol=1)
    usuario_rol = models.UsuarioRol(id_usuario=nuevo_usuario.id_usuario, id_rol=3)
    db.add(usuario_rol)
    db.commit()
    return {"mensaje": "Usuario registrado exitosamente"}

# Inicia sesión y genera un token JWT
@router.post("/login", summary="Iniciar sesión")
def login(datos: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.alias == datos.alias).first()
    if not usuario or not pwd_context.verify(datos.clave, usuario.clave):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    # Obtiene los roles y módulos del usuario
    roles = []
    modulos = {
        "modulo_principal": False,
        "modulo_adopciones": False,
        "modulo_mascotas": False,
        "modulo_cuentas": False
    }
    for ur in usuario.roles:
        if ur.rol.estado:
            roles.append(ur.rol.descripcion)
            for modulo in modulos.keys():
                if getattr(ur.rol, modulo):
                    modulos[modulo] = True
    token_data = {
        "sub": usuario.alias,
        "id_usuario": usuario.id_usuario,
        "roles": roles,
        "modulos": modulos
    }
    token = crear_token(token_data)
    return {"access_token": token, "token_type": "bearer", "roles": roles, "modulos": modulos}

# Cambia la contraseña de un usuario (solo propietario o administrador)
@router.put("/cambiar-clave", summary="Cambiar contraseña")
def cambiar_clave(
    datos: schemas.CambiarClave,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    es_admin = "Administrador" in user.get("roles", [])
    es_propietario = user.get("id_usuario") == datos.id_usuario
    if not (es_admin or es_propietario):
        raise HTTPException(status_code=403, detail="No tienes permisos para cambiar la contraseña de este usuario")
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == datos.id_usuario).first()
    if not usuario or (not es_admin and not pwd_context.verify(datos.clave_actual, usuario.clave)):
        raise HTTPException(status_code=401, detail="Clave actual incorrecta")
    usuario.clave = pwd_context.hash(datos.nueva_clave)
    db.commit()
    return {"mensaje": "Contraseña cambiada correctamente"}

# Cambia las preguntas de seguridad de un usuario (solo propietario o administrador)
@router.put("/cambiar-preguntas", summary="Cambiar preguntas de seguridad")
def cambiar_preguntas(
    datos: schemas.CambiarPreguntas,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    es_admin = "Administrador" in user.get("roles", [])
    es_propietario = user.get("id_usuario") == datos.id_usuario
    if not (es_admin or es_propietario):
        raise HTTPException(status_code=403, detail="No tienes permisos para cambiar las preguntas de este usuario")
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == datos.id_usuario).first()
    if not usuario or (not es_admin and not pwd_context.verify(datos.clave_actual, usuario.clave)):
        raise HTTPException(status_code=401, detail="Clave actual incorrecta")
    usuario.pregunta_seguridad = datos.pregunta_seguridad
    usuario.respuesta_seguridad = datos.respuesta_seguridad
    db.commit()
    return {"mensaje": "Preguntas de seguridad actualizadas correctamente"}

# Cambia el alias de un usuario (solo propietario o administrador)
@router.put("/cambiar-usuario", summary="Cambiar nombre de usuario")
def cambiar_alias(
    datos: schemas.CambiarAlias,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Permitir solo al propietario o al administrador
    es_admin = "Administrador" in user.get("roles", [])
    es_propietario = user.get("id_usuario") == datos.id_usuario
    if not (es_admin or es_propietario):
        raise HTTPException(status_code=403, detail="No tienes permisos para cambiar este alias")
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == datos.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Verifica si el alias ya existe en otro usuario activo
    if db.query(models.Usuario).filter(models.Usuario.alias == datos.nuevo_alias, models.Usuario.id_usuario != datos.id_usuario, models.Usuario.estado == True).first():
        raise HTTPException(status_code=400, detail="El alias ya existe")
    usuario.alias = datos.nuevo_alias
    db.commit()
    return {"mensaje": "Alias actualizado correctamente"}

# Cambiar correo
@router.put("/cambiar-correo", summary="Cambiar correo del usuario")
def cambiar_correo(datos: schemas.CambiarCorreo, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Verifica si el correo ya existe en otro usuario activo
    if db.query(models.Usuario).filter(models.Usuario.correo == datos.nuevo_correo, models.Usuario.id_usuario != usuario.id_usuario, models.Usuario.estado == True).first():
        raise HTTPException(status_code=400, detail="El correo ya existe")
    usuario.correo = datos.nuevo_correo
    db.commit()
    return {"mensaje": "Correo actualizado correctamente"}