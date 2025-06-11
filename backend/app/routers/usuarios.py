from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import crear_token
from ..auth.dependencies import get_current_user, require_roles

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/registro", summary="Registrar un nuevo usuario")
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.alias == usuario.alias).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El alias ya existe")
    hashed_password = pwd_context.hash(usuario.clave)
    nuevo_usuario = models.Usuario(
        alias=usuario.alias,
        clave=hashed_password,
        pregunta_seguridad=usuario.pregunta_seguridad,
        respuesta_seguridad=usuario.respuesta_seguridad
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    # Asigna un rol por defecto (por ejemplo, id_rol=1)
    usuario_rol = models.UsuarioRol(id_usuario=nuevo_usuario.id_usuario, id_rol=1)
    db.add(usuario_rol)
    db.commit()
    return {"mensaje": "Usuario registrado exitosamente"}

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

@router.get("/me", summary="Obtener datos del usuario actual")
def obtener_usuario_actual(user=Depends(get_current_user)):
    return {
        "id_usuario": user.get("id_usuario"),
        "alias": user.get("sub"),
        "roles": user.get("roles"),
        "modulos": user.get("modulos")
    }

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

@router.get("/", summary="Listar usuarios")
def listar_usuarios(db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    usuarios = db.query(models.Usuario).all()
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

@router.put("/actualizar", summary="Actualizar datos del usuario")
def actualizar_usuario(datos: schemas.UsuarioUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if datos.pregunta_seguridad is not None:
        usuario.pregunta_seguridad = datos.pregunta_seguridad
    if datos.respuesta_seguridad is not None:
        usuario.respuesta_seguridad = datos.respuesta_seguridad
    db.commit()
    return {"mensaje": "Datos actualizados correctamente"}

@router.put("/cambiar-clave", summary="Cambiar contraseña")
def cambiar_clave(datos: schemas.CambiarClave, db: Session = Depends(get_db), user=Depends(get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user["id_usuario"]).first()
    if not usuario or not pwd_context.verify(datos.clave_actual, usuario.clave):
        raise HTTPException(status_code=401, detail="Clave actual incorrecta")
    usuario.clave = pwd_context.hash(datos.nueva_clave)
    db.commit()
    return {"mensaje": "Contraseña cambiada correctamente"}

@router.delete("/{id_usuario}", summary="Eliminar usuario lógicamente")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db), user=Depends(require_roles(["Administrador"]))):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if usuario:
        usuario.estado = False
        db.commit()
        return {"mensaje": "Usuario eliminado lógicamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")