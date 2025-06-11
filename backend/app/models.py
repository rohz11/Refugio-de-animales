from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    alias = Column(String(50), unique=True, nullable=False)
    clave = Column(String(255), nullable=False)
    pregunta_seguridad = Column(Text)
    respuesta_seguridad = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    ultimo_login = Column(DateTime)
    
    roles = relationship("UsuarioRol", back_populates="usuario")
    persona = relationship("Persona", back_populates="usuario", uselist=False)
    mascotas_registradas = relationship("Mascota", back_populates="registrador")
    adopciones_solicitadas = relationship("Adopcion", back_populates="usuario", foreign_keys="Adopcion.id_usuario")
    adopciones_entrevistadas = relationship("Adopcion", back_populates="entrevistador", foreign_keys="Adopcion.id_entrevistador")

class Rol(Base):
    __tablename__ = "roles"
    
    id_rol = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(50), nullable=False)
    estado = Column(Boolean, default=True)
    modulo_principal = Column(Boolean, default=False)
    modulo_adopciones = Column(Boolean, default=False)
    modulo_mascotas = Column(Boolean, default=False)
    modulo_cuentas = Column(Boolean, default=False)
    
    usuarios = relationship("UsuarioRol", back_populates="rol")

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"
    
    id_ur = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    id_rol = Column(Integer, ForeignKey('roles.id_rol'))
    descripcion = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol", back_populates="usuarios")

class Persona(Base):
    __tablename__ = "personas"
    
    id_persona = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), unique=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    direccion = Column(Text)
    telefono = Column(String(20))
    dni = Column(String(20), unique=True)
    correo = Column(String(100), unique=True)
    estado = Column(Boolean, default=True)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="persona")
    perfiles_adopcion = relationship("PerfilAdopcion", back_populates="persona")

class Especie(Base):
    __tablename__ = "especies"
    
    id_especie = Column(Integer, primary_key=True, index=True)
    especie = Column(String(50), unique=True, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    mascotas = relationship("Mascota", back_populates="especie")

class Raza(Base):
    __tablename__ = "razas"
    
    id_raza = Column(Integer, primary_key=True, index=True)
    id_especie = Column(Integer, ForeignKey('especies.id_especie'))
    raza = Column(String(50), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    especie = relationship("Especie")
    mascotas = relationship("Mascota", back_populates="raza")

class PerfilAdopcion(Base):
    __tablename__ = "perfil_adopcion"
    
    id_perfil = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey('personas.id_persona'))
    direccion = Column(String(200))
    tipo_vivienda = Column(String(50))
    familia = Column(Text)
    mascota = Column(Boolean)
    dedicacion = Column(Text)
    tiempo_libre = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    adopciones = relationship("Adopcion", back_populates="perfil")
    persona = relationship("Persona", back_populates="perfiles_adopcion")

class Mascota(Base):
    __tablename__ = "mascotas"
    
    id_mascota = Column(Integer, primary_key=True, index=True)
    nombre_mascota = Column(String(100), nullable=False)
    sexo = Column(String(10))
    id_especie = Column(Integer, ForeignKey("especies.id_especie"))
    id_raza = Column(Integer, ForeignKey("razas.id_raza"))
    edad = Column(Integer)
    estado_mascota = Column(String(20))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_regreso = Column(Date)
    registrado_por = Column(Integer, ForeignKey('usuarios.id_usuario'))
    estado = Column(Boolean, default=True)
    
    fotos = relationship("FotoMascota", back_populates="mascota")
    especie = relationship("Especie", back_populates="mascotas")
    raza = relationship("Raza", back_populates="mascotas")
    adopciones = relationship("Adopcion", back_populates="mascota")
    registrador = relationship("Usuario", back_populates="mascotas_registradas")

class FotoMascota(Base):
    __tablename__ = "fotos_mascota"

    id_foto = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey('mascotas.id_mascota'))
    url = Column(String(255), nullable=False)
    descripcion = Column(String(255))
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Mascota", back_populates="fotos")

class Adopcion(Base):
    __tablename__ = "adopciones"
    
    id_adopcion = Column(Integer, primary_key=True, index=True)
    id_perfil = Column(Integer, ForeignKey("perfil_adopcion.id_perfil"))
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"))
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    estado_adopcion = Column(String(20))
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_entrevista = Column(DateTime)
    id_entrevistador = Column(Integer, ForeignKey('usuarios.id_usuario'))
    respuesta = Column(Text)
    estado = Column(Boolean, default=True)
    
    perfil = relationship("PerfilAdopcion", back_populates="adopciones")
    mascota = relationship("Mascota", back_populates="adopciones")
    usuario = relationship("Usuario", foreign_keys=[id_usuario], back_populates="adopciones_solicitadas")
    entrevistador = relationship("Usuario", foreign_keys=[id_entrevistador], back_populates="adopciones_entrevistadas")