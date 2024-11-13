from .jugadores import router as jugadores_router
from .campeonatos import router as campeonatos_router
from .partidas import router as partidas_router
from .resultados import router as resultados_router
from .mesas import router as mesas_router

__all__ = [
    'jugadores_router',
    'campeonatos_router',
    'partidas_router',
    'resultados_router',
    'mesas_router'
] 