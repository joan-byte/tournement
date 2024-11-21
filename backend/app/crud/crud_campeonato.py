# Importaciones necesarias para el módulo
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.campeonato import Campeonato
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate

# Clase que hereda de CRUDBase para manejar operaciones CRUD específicas de Campeonato
# Utiliza tipos genéricos:
# - Campeonato: El modelo SQLAlchemy
# - CampeonatoCreate: Schema Pydantic para crear campeonatos
# - CampeonatoUpdate: Schema Pydantic para actualizar campeonatos
class CRUDCampeonato(CRUDBase[Campeonato, CampeonatoCreate, CampeonatoUpdate]):
    """
    Clase CRUD para gestionar operaciones de base de datos relacionadas con Campeonatos.
    Hereda todas las operaciones básicas de CRUDBase sin necesidad de implementación adicional.
    
    Operaciones disponibles:
    - get: Obtener un campeonato por ID
    - get_multi: Obtener múltiples campeonatos con paginación
    - create: Crear un nuevo campeonato
    - update: Actualizar un campeonato existente
    - remove: Eliminar un campeonato
    """
    pass

# Instancia única de CRUDCampeonato para ser utilizada en toda la aplicación
# Esta instancia proporciona acceso a todas las operaciones CRUD para la entidad Campeonato
campeonato = CRUDCampeonato(Campeonato) 