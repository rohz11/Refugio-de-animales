from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UsuarioCreate(BaseModel):
    alias: str
    clave: str
    pregunta_seguridad: str | None = None
    respuesta_seguridad: str | None = None

class UsuarioLogin(BaseModel):
    alias: str
    clave: str

class UsuarioUpdate(BaseModel):
    pregunta_seguridad: str | None = None
    respuesta_seguridad: str | None = None

class CambiarClave(BaseModel):
    clave_actual: str
    nueva_clave: str
class MascotaCreate(BaseModel):
    nombre_mascota: str
    sexo: Optional[str] = None
    especie_id: int
    raza_id: int
    edad: Optional[int] = None
    estado_mascota: Optional[str] = None
    descripcion: Optional[str] = None

class MascotaUpdate(BaseModel):
    nombre_mascota: Optional[str] = None
    sexo: Optional[str] = None
    especie_id: Optional[int] = None
    raza_id: Optional[int] = None
    edad: Optional[int] = None
    estado_mascota: Optional[str] = None
    descripcion: Optional[str] = None

class FotoMascotaCreate(BaseModel):
    url: str
    descripcion: Optional[str] = None

class FotoMascotaResponse(BaseModel):
    id_foto: int
    url: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class MascotaResponse(BaseModel):
    id_mascota: int
    nombre_mascota: str
    sexo: Optional[str]
    especie_id: int
    raza_id: int
    edad: Optional[int]
    estado_mascota: Optional[str]
    descripcion: Optional[str]
    fotos: List[FotoMascotaResponse] = []

    class Config:
        from_attributes = True  


class AdopcionCreate(BaseModel):
    id_perfil: int
    id_mascota: int

class AsignarEntrevista(BaseModel):
    fecha_entrevista: datetime
    id_entrevistador: int

class CambiarEstadoAdopcion(BaseModel):
    estado_adopcion: str
    respuesta: Optional[str] = None

class AdopcionResponse(BaseModel):
    id_adopcion: int
    id_perfil: int
    id_mascota: int
    id_usuario: int
    estado_adopcion: Optional[str]
    fecha_solicitud: Optional[datetime]
    fecha_entrevista: Optional[datetime]
    id_entrevistador: Optional[int]
    respuesta: Optional[str]
    estado: bool

    class Config:
        from_attributes = True



class PerfilAdopcionCreate(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    informacion_adicional: Optional[str] = None

class PerfilAdopcionUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    informacion_adicional: Optional[str] = None

class PerfilAdopcionResponse(BaseModel):
    id_perfil: int
    id_persona: int
    nombre: str
    direccion: str
    telefono: str
    informacion_adicional: Optional[str]
    estado: bool

    class Config:
        from_attributes = True


# Especie
class EspecieCreate(BaseModel):
    nombre: str

class EspecieUpdate(BaseModel):
    nombre: Optional[str] = None

class EspecieResponse(BaseModel):
    id_especie: int
    nombre: str
    estado: bool

    class Config:
        from_attributes = True

# Raza
class RazaCreate(BaseModel):
    nombre: str
    id_especie: int

class RazaUpdate(BaseModel):
    nombre: Optional[str] = None
    id_especie: Optional[int] = None

class RazaResponse(BaseModel):
    id_raza: int
    nombre: str
    id_especie: int
    estado: bool

    class Config:
        from_attributes = True