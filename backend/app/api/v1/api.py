from fastapi import APIRouter
from app.api.v1.endpoints import (
    campeonatos,
    jugadores,
    mesas,
    parejas,
    resultados,
    estadisticas,
    historial,
    exportacion
)

api_router = APIRouter()

api_router.include_router(
    campeonatos.router,
    prefix="/campeonatos",
    tags=["campeonatos"]
)

api_router.include_router(
    jugadores.router,
    prefix="/jugadores",
    tags=["jugadores"]
)

api_router.include_router(
    mesas.router,
    prefix="/mesas",
    tags=["mesas"]
)

api_router.include_router(
    parejas.router,
    prefix="/parejas",
    tags=["parejas"]
)

api_router.include_router(
    resultados.router,
    prefix="/resultados",
    tags=["resultados"]
)

api_router.include_router(
    estadisticas.router,
    prefix="/estadisticas",
    tags=["estadisticas"]
)

api_router.include_router(
    historial.router,
    prefix="/historial",
    tags=["historial"]
)

api_router.include_router(
    exportacion.router,
    prefix="/exportar",
    tags=["exportacion"]
) 