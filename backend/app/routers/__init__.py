from .campeonatos import router as campeonatos
from .parejas import router as parejas
from .jugadores import router as jugadores
from .mesas import router as mesas
from .partidas import router as partidas
from .resultados import router as resultados

__all__ = [
    'campeonatos',
    'parejas',
    'jugadores',
    'mesas',
    'partidas',
    'resultados'
] 