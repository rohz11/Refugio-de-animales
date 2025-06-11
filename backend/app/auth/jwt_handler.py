from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "TU_SECRETO"  # Cambia esto y usa variables de entorno en producción
ALGORITHM = "HS256"

def crear_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)