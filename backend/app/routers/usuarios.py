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
    # Verifica si el alias ya existe
    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.alias == usuario.alias,
        models.Usuario.estado == True
    ).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El alias ya existe")

    db_persona = db.query(models.Persona).filter(
        models.Persona.correo == usuario.persona.correo,
        models.Persona.estado == True
    ).first()
    if db_persona:
        raise HTTPException(status_code=400, detail="El correo ya existe")

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
        pregunta_seguridad=usuario.pregunta_seguridad,
        respuesta_seguridad=usuario.respuesta_seguridad,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # 2. Crea la persona asociada a ese usuario
    persona = models.Persona(
        id_usuario=nuevo_usuario.id_usuario,
        nombre=usuario.persona.nombre,
        apellido=usuario.persona.apellido,
        dni=usuario.persona.dni,
        telefono=usuario.persona.telefono,
        correo=usuario.persona.correo,
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

# Obtiene los datos del usuario actual
@router.get("/me", summary="Obtener datos del usuario actual")
def obtener_usuario_actual(user=Depends(get_current_user)):
    return {
        "id_usuario": user.get("id_usuario"),
        "alias": user.get("sub"),
        "roles": user.get("roles"),
        "modulos": user.get("modulos")
    }

# Cambia la contraseña del usuario actual
@router.put("/cambiar-clave", summary="Cambiar contraseña")
def cambiar_clave(datos: schemas.CambiarClave, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not pwd_context.verify(datos.clave_actual, usuario.clave):
        raise HTTPException(status_code=401, detail="Clave actual incorrecta")
    usuario.clave = pwd_context.hash(datos.nueva_clave)
    db.commit()
    return {"mensaje": "Contraseña cambiada correctamente"}

# Cambia las preguntas de seguridad del usuario actual
@router.put("/cambiar-preguntas", summary="Cambiar preguntas de seguridad")
def cambiar_preguntas(
    datos: schemas.CambiarPreguntas,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not pwd_context.verify(datos.clave_actual, usuario.clave):
        raise HTTPException(status_code=401, detail="Clave actual incorrecta")
    usuario.pregunta_seguridad = datos.pregunta_seguridad
    usuario.respuesta_seguridad = datos.respuesta_seguridad
    db.commit()
    return {"mensaje": "Preguntas de seguridad actualizadas correctamente"}

# Cambia el alias del usuario actual
@router.put("/cambiar-usuario", summary="Cambiar nombre de usuario")
def cambiar_alias(datos: schemas.CambiarAlias, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Verifica si el alias ya existe
    if db.query(models.Usuario).filter(models.Usuario.alias == datos.nuevo_alias).first():
        raise HTTPException(status_code=400, detail="El alias ya existe")
    usuario.alias = datos.nuevo_alias
    db.commit()
    return {"mensaje": "Alias actualizado correctamente"}

# Asigna un rol a un usuario (solo para administradores)
@router.post("/asignar-rol", summary="Asignar rol a un usuario")
def asignar_rol(id_usuario: int, id_rol: int, db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    rol = db.query(models.Rol).filter(models.Rol.id_rol == id_rol).first()
    if not usuario or not rol:
        raise HTTPException(status_code=404, detail="Usuario o rol no encontrado")
    # Verifica si ya tiene ese rol
    existe = db.query(models.UsuarioRol).filter_by(id_usuario=id_usuario, id_rol=id_rol).first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya tiene este rol")
    usuario_rol = models.UsuarioRol(id_usuario=id_usuario, id_rol=id_rol)
    db.add(usuario_rol)
    db.commit()
    return {"mensaje": "Rol asignado correctamente"}

# Listar usuarios activos
@router.get("/", summary="Listar usuarios")
def listar_usuarios(db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    usuarios = db.query(models.Usuario).filter(models.Usuario.estado == True).all()
    resultado = []
    for u in usuarios:
        roles = [ur.rol.descripcion for ur in u.roles if ur.rol.estado]
        resultado.append({
            "id_usuario": u.id_usuario,
            "alias": u.alias,
            "estado": u.estado,
            "roles": roles
        })
    return resultado

# Elimina un usuario lógicamente (cambia su estado a False)
@router.delete("/{id_usuario}", summary="Eliminar usuario lógicamente")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.estado = False
    # Elimina lógicamente la persona asociada
    if usuario.persona:
        usuario.persona.estado = False
        # Elimina lógicamente los perfiles de adopción asociados
        for perfil in usuario.persona.perfiles_adopcion:
            perfil.estado = False
    # Elimina lógicamente los roles asociados
    for usuario_rol in usuario.roles:
        usuario_rol.estado = False
    db.commit()
    return {"mensaje": "Usuario, persona, roles y datos relacionados eliminados lógicamente"}

# Datos personas
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

# Cambiar correo
@router.put("/cambiar-correo", summary="Cambiar correo de la persona")
def cambiar_correo(datos: schemas.CambiarCorreo, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not usuario.persona:
        raise HTTPException(status_code=404, detail="Usuario o persona no encontrado")
    # Verifica si el correo ya existe
    if db.query(models.Persona).filter(models.Persona.correo == datos.nuevo_correo).first():
        raise HTTPException(status_code=400, detail="El correo ya existe")
    usuario.persona.correo = datos.nuevo_correo
    db.commit()
    return {"mensaje": "Correo actualizado correctamente"}

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
            "correo": p.correo,
            "telefono": p.telefono,
            "direccion": p.direccion,
            "estado": p.estado
        })
    return resultado

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