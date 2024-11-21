# Importaciones necesarias para la aplicación FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    campeonatos,
    parejas,
    jugadores,
    mesas,
    partidas,
    resultados,
    ranking
)

# Creación de la instancia principal de la aplicación FastAPI
app = FastAPI()

# Configuración del middleware CORS (Cross-Origin Resource Sharing)
# Permite que el frontend acceda a la API desde un origen diferente
app.add_middleware(
    CORSMiddleware,
    # Lista de orígenes permitidos para realizar peticiones
    allow_origins=["http://localhost:8080"],
    # Permite el envío de credenciales (cookies, headers de autorización)
    allow_credentials=True,
    # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    # Permite todos los headers en las peticiones
    allow_headers=["*"],
)

# Inclusión de los diferentes routers de la aplicación
# Cada router maneja un conjunto específico de endpoints relacionados
app.include_router(
    campeonatos,
    prefix="/api/campeonatos",
    tags=["campeonatos"]  # Tag para agrupar endpoints en la documentación
)
app.include_router(
    parejas,
    prefix="/api/parejas",
    tags=["parejas"]
)
app.include_router(
    jugadores,
    prefix="/api/jugadores",
    tags=["jugadores"]
)
app.include_router(
    mesas,
    prefix="/api/mesas",
    tags=["mesas"]
)
app.include_router(
    partidas,
    prefix="/api/partidas",
    tags=["partidas"]
)
app.include_router(
    resultados,
    prefix="/api/resultados",
    tags=["resultados"]
)
app.include_router(
    ranking.router,
    prefix="/api/ranking",
    tags=["ranking"]
)

# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def read_root():
    """
    Endpoint de prueba que confirma que la API está funcionando.
    
    Returns:
        dict: Mensaje simple de confirmación
    """
    return {"Hello": "World"}
