from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import crear_token
from ..auth.dependencies import get_current_user, require_roles

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Obtiene los datos del usuario actual
@router.get("/me", summary="Obtener datos del usuario actual")
def obtener_usuario_actual(user=Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == user.get("id_usuario")).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "id_usuario": usuario.id_usuario,
        "alias": usuario.alias,
        "correo": usuario.correo,
        "roles": user.get("roles"),
        "modulos": user.get("modulos")
    }

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
            "correo": u.correo,
            "estado": u.estado,
            "roles": roles
        })
    return resultado


# Puedes dejarlo vacío por ahora o agregar endpoints después# Asigna un rol a un usuario (solo para administradores)
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


# Elimina un usuario lógicamente (cambia su estado a False)
@router.delete("/{id_usuario}", summary="Eliminar usuario lógicamente")
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Solo el propietario o un administrador pueden eliminar
    es_admin = "Administrador" in user.get("roles", [])
    es_propietario = user.get("id_usuario") == id_usuario
    if not (es_admin or es_propietario):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este usuario")

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