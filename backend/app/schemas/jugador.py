from pydantic import BaseModel
from typing import Optional

# Esquema base para Jugador
class JugadorBase(BaseModel):
    nombre: str
    apellido: str

# Esquema para crear un Jugador
class JugadorCreate(JugadorBase):
    pass

# Esquema para actualizar un Jugador
class JugadorUpdate(JugadorBase):
    nombre: Optional[str] = None
    apellido: Optional[str] = None

# Esquema para devolver un Jugador
class JugadorResponse(JugadorBase):
    id: int
    pareja_id: int
    campeonato_id: int

    class Config:
        from_attributes = True

# Esquemas para Pareja
class ParejaBase(BaseModel):
    club: Optional[str] = None
    campeonato_id: int

class JugadorParejaUpdate(BaseModel):
    nombre: str
    apellido: str

class ParejaUpdate(BaseModel):
    club: Optional[str] = None
    activa: Optional[bool] = None
    jugador1: Optional[JugadorParejaUpdate] = None
    jugador2: Optional[JugadorParejaUpdate] = None

    class Config:
        from_attributes = True

class ParejaCreate(ParejaBase):
    jugador1: JugadorCreate
    jugador2: JugadorCreate

class ParejaResponse(ParejaBase):
    id: int
    nombre: str
    activa: bool
    numero: Optional[int] = None

    class Config:
        from_attributes = True
