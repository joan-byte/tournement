from pydantic import BaseModel
from typing import Optional

class RankingResultado(BaseModel):
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
