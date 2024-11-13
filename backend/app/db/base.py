from app.db.base_class import Base
from app.models.campeonato import Campeonato
from app.models.jugador import Jugador
from app.models.pareja import Pareja
from app.models.mesa import Mesa
from app.models.resultado import Resultado

# Exportar Base para que otros módulos puedan importarlo
__all__ = ['Base']
