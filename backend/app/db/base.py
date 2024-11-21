# Este archivo sirve como punto central de importación para todos los modelos SQLAlchemy
# Importa la clase Base que servirá como clase base para todos los modelos
from app.db.base_class import Base

# Importaciones de todos los modelos de la aplicación
# Estas importaciones son necesarias para que Alembic detecte los modelos
# y pueda generar las migraciones correctamente
from app.models.campeonato import Campeonato  # Modelo para gestionar campeonatos
from app.models.jugador import Jugador        # Modelo para gestionar jugadores
from app.models.pareja import Pareja          # Modelo para gestionar parejas
from app.models.mesa import Mesa              # Modelo para gestionar mesas de juego
from app.models.resultado import Resultado     # Modelo para gestionar resultados

# Lista de exportación que hace que Base esté disponible cuando se importa este módulo
# Esto permite que otros módulos importen Base directamente desde aquí
__all__ = ['Base']

"""
Este módulo actúa como un punto de entrada centralizado para todos los modelos SQLAlchemy.
Tiene dos propósitos principales:

1. Asegurar que todos los modelos están registrados correctamente con SQLAlchemy
   al importarlos en un solo lugar.

2. Proporcionar un punto único de importación para la clase Base, que es la clase
   base para todos los modelos SQLAlchemy en la aplicación.

Nota: Es importante mantener actualizadas las importaciones cuando se añadan
      nuevos modelos a la aplicación.
"""
