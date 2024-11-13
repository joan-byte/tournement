from pydantic import BaseModel
from typing import Optional, List
from .jugador import JugadorCreate, JugadorResponse

class ParejaBase(BaseModel):
    nombre: str
    club: Optional[str] = None
    campeonato_id: int
    activa: bool = True

class JugadorParejaCreate(BaseModel):
    nombre: str
    apellido: str

class ParejaCreate(ParejaBase):
    jugador1: JugadorParejaCreate
    jugador2: JugadorParejaCreate

class ParejaUpdate(BaseModel):
    nombre: Optional[str] = None
    club: Optional[str] = None
    activa: Optional[bool] = None
    jugador1: Optional[JugadorParejaCreate] = None
    jugador2: Optional[JugadorParejaCreate] = None

class ParejaResponse(ParejaBase):
    id: int
    numero: int
    jugadores: List[JugadorResponse] = []

    class Config:
        from_attributes = True

class ParejaSimple(BaseModel):
    id: int
    nombre: str
    club: Optional[str] = None

    class Config:
        from_attributes = True
