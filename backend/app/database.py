# Importamos las clases necesarias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuración de la URL de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://one:rohz1234@localhost:3999/refugio_wsc"
# Ejemplo para MySQL: "mysql+pymysql://usuario:contraseña@localhost/nombre_db"

# 2. Creación del motor (engine) de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica que la conexión esté activa antes de usarla
    echo=True  # Opcional: Muestra logs de SQL en consola (útil para desarrollo)
)

# 3. Configuración de la sesión local
SessionLocal = sessionmaker(
    autocommit=False,  # Desactiva el autocommit (mejor control)
    autoflush=False,   # Desactiva el autoflush (evita comportamientos inesperados)
    bind=engine        # Vincula la sesión al motor
)

# 4. Base para los modelos de SQLAlchemy
Base = declarative_base()