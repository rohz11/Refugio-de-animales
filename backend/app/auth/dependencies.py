from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from ..auth.jwt_handler import SECRET_KEY, ALGORITHM

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

def require_roles(roles_permitidos: list):
    def role_checker(user=Depends(get_current_user)):
        user_roles = user.get("roles", [])
        if not any(role in roles_permitidos for role in user_roles):
            raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
        return user
    return role_checker
