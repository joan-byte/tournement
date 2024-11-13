from fastapi import APIRouter
from app.api.v1.endpoints import campeonatos, jugadores, parejas, mesas, resultados

api_router = APIRouter()

api_router.include_router(campeonatos.router, prefix="/campeonatos", tags=["campeonatos"])
api_router.include_router(jugadores.router, prefix="/jugadores", tags=["jugadores"])
api_router.include_router(parejas.router, prefix="/parejas", tags=["parejas"])
api_router.include_router(mesas.router, prefix="/mesas", tags=["mesas"])
api_router.include_router(resultados.router, prefix="/resultados", tags=["resultados"])
