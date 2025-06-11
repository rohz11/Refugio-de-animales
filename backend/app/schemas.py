from pydantic import BaseModel
from typing import Optional, List

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