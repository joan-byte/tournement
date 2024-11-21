# Importaciones necesarias para definir los esquemas de datos
from pydantic import BaseModel
from typing import Optional

class MesaBase(BaseModel):
    """
    Esquema base para el modelo Mesa.
    Define los campos fundamentales que describen una mesa de juego.
    
    Attributes:
        numero (int): Número identificativo de la mesa en el campeonato
        campeonato_id (int): ID del campeonato al que pertenece la mesa
        partida (int): Número de la partida en la que se juega
        pareja1_id (int): ID de la primera pareja asignada a la mesa
        pareja2_id (Optional[int]): ID de la segunda pareja (puede ser None si es mesa libre)
    """
    numero: int
    campeonato_id: int
    partida: int
    pareja1_id: int
    pareja2_id: Optional[int] = None

class MesaCreate(MesaBase):
    """
    Esquema para crear una nueva mesa.
    Hereda todos los campos de MesaBase sin modificaciones adicionales.
    Se utiliza para validar los datos de entrada al crear una mesa.
    """
    pass

class MesaUpdate(BaseModel):
    """
    Esquema para actualizar una mesa existente.
    Solo permite actualizar las parejas asignadas a la mesa.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    
    Attributes:
        pareja1_id (Optional[int]): Nueva primera pareja
        pareja2_id (Optional[int]): Nueva segunda pareja
    """
    pareja1_id: Optional[int] = None
    pareja2_id: Optional[int] = None

class MesaResponse(MesaBase):
    """
    Esquema para la respuesta de la API con información básica de la mesa.
    Añade el ID a los campos base de la mesa.
    
    Attributes:
        id (int): Identificador único de la mesa
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    id: int

    class Config:
        from_attributes = True

class MesaConParejas(MesaResponse):
    """
    Esquema extendido para respuesta de API que incluye información de las parejas.
    Útil para mostrar los nombres de las parejas asignadas a la mesa.
    
    Attributes:
        pareja1_nombre (Optional[str]): Nombre de la primera pareja
        pareja2_nombre (Optional[str]): Nombre de la segunda pareja
        tiene_resultados (bool): Indica si la mesa ya tiene resultados registrados
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    pareja1_nombre: Optional[str] = None
    pareja2_nombre: Optional[str] = None
    tiene_resultados: bool = False

    class Config:
        from_attributes = True
