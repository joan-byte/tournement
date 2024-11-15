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

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(campeonatos, prefix="/api/campeonatos", tags=["campeonatos"])
app.include_router(parejas, prefix="/api/parejas", tags=["parejas"])
app.include_router(jugadores, prefix="/api/jugadores", tags=["jugadores"])
app.include_router(mesas, prefix="/api/mesas", tags=["mesas"])
app.include_router(partidas, prefix="/api/partidas", tags=["partidas"])
app.include_router(resultados, prefix="/api/resultados", tags=["resultados"])
app.include_router(ranking.router, prefix="/api/ranking", tags=["ranking"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
