from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.jugadores import router as jugadores_router
from app.routers.campeonatos import router as campeonatos_router
from app.routers.partidas import router as partidas_router
from app.routers.resultados import router as resultados_router
from app.routers.mesas import router as mesas_router

app = FastAPI()

# Configurar CORS - Actualizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

# Incluir los routers
app.include_router(jugadores_router, prefix="/api", tags=["jugadores"])
app.include_router(campeonatos_router, prefix="/api/campeonatos", tags=["campeonatos"])
app.include_router(partidas_router, prefix="/api/partidas", tags=["partidas"])
app.include_router(resultados_router, prefix="/api/resultados", tags=["resultados"])
app.include_router(mesas_router, prefix="/api/mesas", tags=["mesas"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
