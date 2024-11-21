# Importaciones necesarias para definir los esquemas de datos
from pydantic import BaseModel
from typing import Optional, List
from .jugador import JugadorCreate, JugadorResponse

class ParejaBase(BaseModel):
    """
    Esquema base para el modelo Pareja.
    Define los campos fundamentales que describen una pareja en el campeonato.
    
    Attributes:
        nombre (str): Nombre identificativo de la pareja
        club (Optional[str]): Club al que pertenece la pareja (opcional)
        campeonato_id (int): ID del campeonato al que pertenece
        activa (bool): Estado de participación de la pareja (default True)
    """
    nombre: str
    club: Optional[str] = None
    campeonato_id: int
    activa: bool = True

class JugadorParejaCreate(BaseModel):
    """
    Esquema para crear un jugador dentro del contexto de una pareja.
    Contiene los datos básicos necesarios para identificar a un jugador.
    
    Attributes:
        nombre (str): Nombre del jugador
        apellido (str): Apellido del jugador
    """
    nombre: str
    apellido: str

class ParejaCreate(ParejaBase):
    """
    Esquema para crear una nueva pareja.
    Extiende ParejaBase añadiendo la información de ambos jugadores.
    
    Attributes:
        jugador1 (JugadorParejaCreate): Datos del primer jugador
        jugador2 (JugadorParejaCreate): Datos del segundo jugador
    """
    jugador1: JugadorParejaCreate
    jugador2: JugadorParejaCreate

class ParejaUpdate(BaseModel):
    """
    Esquema para actualizar una pareja existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    
    Attributes:
        nombre (Optional[str]): Nuevo nombre de la pareja
        club (Optional[str]): Nuevo club de la pareja
        activa (Optional[bool]): Nuevo estado de participación
        jugador1 (Optional[JugadorParejaCreate]): Nuevos datos del primer jugador
        jugador2 (Optional[JugadorParejaCreate]): Nuevos datos del segundo jugador
    """
    nombre: Optional[str] = None
    club: Optional[str] = None
    activa: Optional[bool] = None
    jugador1: Optional[JugadorParejaCreate] = None
    jugador2: Optional[JugadorParejaCreate] = None

class ParejaResponse(ParejaBase):
    """
    Esquema para la respuesta de la API con información completa de la pareja.
    Incluye todos los campos base más información adicional.
    
    Attributes:
        id (int): Identificador único de la pareja
        numero (int): Número asignado a la pareja en el campeonato
        jugadores (List[JugadorResponse]): Lista de jugadores que forman la pareja
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    id: int
    numero: int
    jugadores: List[JugadorResponse] = []

    class Config:
        from_attributes = True

class ParejaSimple(BaseModel):
    """
    Esquema simplificado de pareja para respuestas que requieren información básica.
    Útil para listados y referencias simples.
    
    Attributes:
        id (int): Identificador único de la pareja
        nombre (str): Nombre de la pareja
        club (Optional[str]): Club al que pertenece
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    id: int
    nombre: str
    club: Optional[str] = None

    class Config:
        from_attributes = True
