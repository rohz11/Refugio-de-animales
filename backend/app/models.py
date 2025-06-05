from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, Boolean, Text
from sqlalchemy.orm import relationship
from .database import Base

# Tablas independientes (sin FK)
class Rol(Base):
    __tablename__ = "roles"
    id_rol = Column(Integer, primary_key=True, index=True)
    rol = Column(String(20), unique=True, nullable=False)
    usuarios = relationship("Usuario", back_populates="rol")

class Especie(Base):
    __tablename__ = "especies"
    id_especie = Column(Integer, primary_key=True, index=True)
    especie = Column(String(50), unique=True, nullable=False)
    mascotas = relationship("Mascota", back_populates="especie")

class Raza(Base):
    __tablename__ = "razas"
    id_raza = Column(Integer, primary_key=True, index=True)
    raza = Column(String(50), unique=True, nullable=False)
    mascotas = relationship("Mascota", back_populates="raza")

# Tablas dependientes
class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100), unique=True, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    rol = relationship("Rol", back_populates="usuarios")
    adopciones = relationship("Adopcion", back_populates="usuario", foreign_keys="Adopcion.id_usuario")
    entrevistas = relationship("Adopcion", back_populates="entrevistador", foreign_keys="Adopcion.id_entrevistador")

class PerfilAdopcion(Base):
    __tablename__ = "perfil_adopcion"
    id_perfil = Column(Integer, primary_key=True, index=True)
    direccion = Column(String(200))
    tipo_vivienda = Column(String(50))
    familia = Column(Text)
    mascota = Column(Boolean)
    dedicacion = Column(Text)
    tiempo_libre = Column(Text)
    adopciones = relationship("Adopcion", back_populates="perfil")

class Mascota(Base):
    __tablename__ = "mascotas"
    id_mascota = Column(Integer, primary_key=True, index=True)
    nombre_mascota = Column(String(100), nullable=False)
    sexo = Column(String(10))
    id_especie = Column(Integer, ForeignKey("especies.id_especie"))
    id_raza = Column(Integer, ForeignKey("razas.id_raza"))
    edad = Column(Integer)
    estado_mascota = Column(String(20))  # Ej: "Disponible", "Adoptado"
    foto = Column(String(255))  # URL o path a la imagen
    fecha_regreso = Column(Date)
    registrado_por = Column(Integer, ForeignKey("usuarios.id_usuario"))
    especie = relationship("Especie", back_populates="mascotas")
    raza = relationship("Raza", back_populates="mascotas")
    adopciones = relationship("Adopcion", back_populates="mascota")

class Adopcion(Base):
    __tablename__ = "adopciones"
    id_adopcion = Column(Integer, primary_key=True, index=True)
    id_perfil = Column(Integer, ForeignKey("perfil_adopcion.id_perfil"))
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    estado_adopcion = Column(String(20))  # Ej: "Pendiente", "Aprobada"
    fecha_solicitud = Column(Date, nullable=False)
    fecha_entrevista = Column(Date)
    id_entrevistador = Column(Integer, ForeignKey("usuarios.id_usuario"))
    respuesta = Column(Text)
    perfil = relationship("PerfilAdopcion", back_populates="adopciones")
    mascota = relationship("Mascota", back_populates="adopciones")
    usuario = relationship("Usuario", back_populates="adopciones", foreign_keys=[id_usuario])
    entrevistador = relationship("Usuario", back_populates="entrevistas", foreign_keys=[id_entrevistador])