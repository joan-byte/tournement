# Importaciones necesarias para definir los esquemas de datos
from pydantic import BaseModel
from typing import Optional

class ResultadoPareja(BaseModel):
    id: int
    RP: int
    PG: int
    PP: int
    GB: str

class ResultadoCreate(BaseModel):
    mesa_id: int
    campeonato_id: int
    partida: int
    pareja1: ResultadoPareja
    pareja2: Optional[ResultadoPareja] = None

class ResultadoResponse(BaseModel):
    pareja1: ResultadoPareja
    pareja2: Optional[ResultadoPareja] = None

    class Config:
        from_attributes = True

class RankingResultado(BaseModel):
    """
    Esquema para representar el resultado de una pareja en el ranking.
    Define la estructura de datos para mostrar la posición y estadísticas
    de una pareja en el ranking del campeonato.
    
    Attributes:
        posicion (int): Posición actual en el ranking (default 0)
        GB (str): Indicador de grupo ('A' por defecto)
        PG (int): Partidas ganadas (default 0)
        PP (int): Puntos perdidos (default 0)
        ultima_partida (int): Número de la última partida jugada (default 1)
        numero (int): Número asignado a la pareja en el campeonato
        nombre (str): Nombre de la pareja
        club (Optional[str]): Club al que pertenece la pareja (opcional)
        pareja_id (int): Identificador único de la pareja
        
    Config:
        from_attributes: Permite la conversión automática desde objetos ORM
        arbitrary_types_allowed: Permite tipos arbitrarios en el modelo
        orm_mode: Habilita el modo ORM para la conversión de datos
    """
    posicion: int = 0
    GB: str = 'A'
    PG: int = 0
    PP: int = 0
    ultima_partida: int = 1
    numero: int
    nombre: str
    club: Optional[str] = None
    pareja_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        orm_mode = True
