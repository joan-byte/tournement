from pydantic import BaseModel
from typing import Optional

# Esquema base para Jugador
class JugadorBase(BaseModel):
    """
    Esquema base para el modelo Jugador.
    Define los campos básicos que identifican a un jugador.
    
    Attributes:
        nombre (str): Nombre del jugador
        apellido (str): Apellido del jugador
    """
    nombre: str
    apellido: str

# Esquema para crear un Jugador
class JugadorCreate(JugadorBase):
    """
    Esquema para crear un nuevo jugador.
    Hereda los campos básicos sin modificaciones adicionales.
    Se utiliza para validar los datos de entrada al crear un jugador.
    """
    pass

# Esquema para actualizar un Jugador
class JugadorUpdate(JugadorBase):
    """
    Esquema para actualizar un jugador existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    
    Attributes:
        nombre (Optional[str]): Nuevo nombre del jugador
        apellido (Optional[str]): Nuevo apellido del jugador
    """
    nombre: Optional[str] = None
    apellido: Optional[str] = None

# Esquema para devolver un Jugador
class JugadorResponse(JugadorBase):
    """
    Esquema para la respuesta de la API con información completa del jugador.
    Incluye los campos base más los identificadores de relaciones.
    
    Attributes:
        id (int): Identificador único del jugador
        pareja_id (int): ID de la pareja a la que pertenece
        campeonato_id (int): ID del campeonato en el que participa
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    id: int
    pareja_id: int
    campeonato_id: int

    class Config:
        from_attributes = True

# Esquemas para Pareja
class ParejaBase(BaseModel):
    """
    Esquema base para el modelo Pareja.
    Define los campos básicos de una pareja.
    
    Attributes:
        club (Optional[str]): Club al que pertenece la pareja
        campeonato_id (int): ID del campeonato en el que participa
    """
    club: Optional[str] = None
    campeonato_id: int

class JugadorParejaUpdate(BaseModel):
    """
    Esquema para actualizar los datos de un jugador dentro de una pareja.
    
    Attributes:
        nombre (str): Nombre del jugador
        apellido (str): Apellido del jugador
    """
    nombre: str
    apellido: str

class ParejaUpdate(BaseModel):
    """
    Esquema para actualizar una pareja existente.
    Permite actualizar tanto datos de la pareja como de sus jugadores.
    
    Attributes:
        club (Optional[str]): Nuevo club de la pareja
        activa (Optional[bool]): Nuevo estado de la pareja
        jugador1 (Optional[JugadorParejaUpdate]): Datos actualizados del primer jugador
        jugador2 (Optional[JugadorParejaUpdate]): Datos actualizados del segundo jugador
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    club: Optional[str] = None
    activa: Optional[bool] = None
    jugador1: Optional[JugadorParejaUpdate] = None
    jugador2: Optional[JugadorParejaUpdate] = None

    class Config:
        from_attributes = True

class ParejaCreate(ParejaBase):
    """
    Esquema para crear una nueva pareja.
    Incluye los datos de ambos jugadores que formarán la pareja.
    
    Attributes:
        jugador1 (JugadorCreate): Datos del primer jugador
        jugador2 (JugadorCreate): Datos del segundo jugador
    """
    jugador1: JugadorCreate
    jugador2: JugadorCreate

class ParejaResponse(ParejaBase):
    """
    Esquema para la respuesta de la API con información completa de la pareja.
    
    Attributes:
        id (int): Identificador único de la pareja
        nombre (str): Nombre compuesto de la pareja
        activa (bool): Estado de la pareja en el campeonato
        numero (Optional[int]): Número asignado a la pareja
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    id: int
    nombre: str
    activa: bool
    numero: Optional[int] = None

    class Config:
        from_attributes = True
