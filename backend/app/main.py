from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importa los routers (debes crearlos en la carpeta routers)
from .routers import usuarios, mascotas, adopciones, especies, razas, perfil_adopcion, personas
from .auth import security

app = FastAPI(
    title="Sistema de Refugio de Animales",
    description="API para la gestión de usuarios, roles, mascotas y adopciones.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto por los dominios de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los routers principales
app.include_router(security.router, prefix="/security", tags=["Seguridad"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(personas.router, prefix="/personas", tags=["Personas"])
app.include_router(mascotas.router, prefix="/mascotas", tags=["Mascotas"])
app.include_router(adopciones.router, prefix="/adopciones", tags=["Adopciones"])
app.include_router(especies.router, prefix="/especies", tags=["Especies"])
app.include_router(razas.router, prefix="/razas", tags=["Razas"])
app.include_router(perfil_adopcion.router, prefix="/perfil-adopcion", tags=["Perfil Adopción"])


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API del Refugio de Animales"}