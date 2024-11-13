from pydantic import BaseModel
from typing import Optional

# Esquema base para Jugador
class JugadorBase(BaseModel):
    nombre: str
    apellido: str
    campeonato_id: int
    pareja_id: Optional[int] = None

# Esquema para crear un Jugador
class JugadorCreate(JugadorBase):
    pass

# Esquema para actualizar un Jugador
class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    pareja_id: Optional[int] = None

# Esquema para devolver un Jugador
class JugadorResponse(JugadorBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Pareja
class ParejaBase(BaseModel):
    club: str
    activa: bool = True
    campeonato_id: int

class ParejaCreate(ParejaBase):
    jugador1_id: int
    jugador2_id: int

class ParejaUpdate(ParejaBase):
    pass

class Pareja(ParejaBase):
    id: int
    jugador1_id: int
    jugador2_id: int
    nombre: str  # Se generará automáticamente: "nombre1 apellido1 y nombre2 apellido2"

    class Config:
        from_attributes = True

# Esquema para devolver una pareja con información de la mesa
class ParejaConMesa(Pareja):
    mesa_numero: Optional[int] = None
