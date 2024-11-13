from pydantic import BaseModel
from datetime import date
from typing import Optional

class CampeonatoBase(BaseModel):
    nombre: str
    fecha_inicio: date
    dias_duracion: int
    numero_partidas: int
    grupo_b: bool = False
    partida_actual: int = 0

class CampeonatoCreate(CampeonatoBase):
    pass

class CampeonatoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    dias_duracion: Optional[int] = None
    numero_partidas: Optional[int] = None
    grupo_b: Optional[bool] = None
    partida_actual: Optional[int] = None

class Campeonato(CampeonatoBase):
    id: int

    class Config:
        from_attributes = True
