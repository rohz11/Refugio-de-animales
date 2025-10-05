# Importamos las clases necesarias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuración de la URL de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:fifi19@localhost:5432/refugio"
# Ejemplo para MySQL: "mysql+pymysql://usuario:contraseña@localhost/nombre_db"

# 2. Creación del motor (engine) de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica que la conexión esté activa antes de usarla
    # Opcional: Muestra logs de SQL en consola (útil para desarrollo)
    echo=True
)

# 3. Configuración de la sesión local
SessionLocal = sessionmaker(
    autocommit=False,  # Desactiva el autocommit (mejor control)
    # Desactiva el autoflush (evita comportamientos inesperados)
    autoflush=False,
    bind=engine        # Vincula la sesión al motor
)

# 4. Base para los modelos de SQLAlchemy
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
