# Importaciones necesarias para definir los esquemas de datos
from pydantic import BaseModel
from datetime import date
from typing import Optional

class CampeonatoBase(BaseModel):
    """
    Esquema base para el modelo Campeonato.
    Define los campos comunes que serán heredados por otros esquemas.
    
    Attributes:
        nombre (str): Nombre del campeonato
        fecha_inicio (date): Fecha en que inicia el campeonato
        dias_duracion (int): Duración total del campeonato en días
        numero_partidas (int): Cantidad total de partidas programadas
        grupo_b (bool): Indica si el campeonato tiene grupo B (default False)
        partida_actual (int): Número de la partida en curso (default 0)
    """
    nombre: str
    fecha_inicio: date
    dias_duracion: int
    numero_partidas: int
    grupo_b: bool = False
    partida_actual: int = 0

class CampeonatoCreate(CampeonatoBase):
    """
    Esquema para crear un nuevo campeonato.
    Hereda todos los campos de CampeonatoBase sin modificaciones adicionales.
    Se utiliza para validar los datos de entrada al crear un campeonato.
    """
    pass

class CampeonatoUpdate(BaseModel):
    """
    Esquema para actualizar un campeonato existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    
    Attributes:
        nombre (Optional[str]): Nuevo nombre del campeonato
        fecha_inicio (Optional[date]): Nueva fecha de inicio
        dias_duracion (Optional[int]): Nueva duración en días
        numero_partidas (Optional[int]): Nuevo número de partidas
        grupo_b (Optional[bool]): Nuevo estado de grupo B
        partida_actual (Optional[int]): Nueva partida actual
    """
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    dias_duracion: Optional[int] = None
    numero_partidas: Optional[int] = None
    grupo_b: Optional[bool] = None
    partida_actual: Optional[int] = None

class Campeonato(CampeonatoBase):
    """
    Esquema completo del campeonato que incluye el ID.
    Se utiliza para las respuestas de la API.
    
    Attributes:
        id (int): Identificador único del campeonato
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
    """
    id: int

    class Config:
        from_attributes = True
