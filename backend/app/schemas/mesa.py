from pydantic import BaseModel
from typing import Optional

class MesaBase(BaseModel):
    numero: int
    campeonato_id: int
    partida: int
    pareja1_id: int
    pareja2_id: Optional[int] = None

class MesaCreate(MesaBase):
    pass

class MesaUpdate(BaseModel):
    pareja1_id: Optional[int] = None
    pareja2_id: Optional[int] = None

class MesaResponse(MesaBase):
    id: int

    class Config:
        from_attributes = True

class MesaConParejas(MesaResponse):
    pareja1_nombre: Optional[str] = None
    pareja2_nombre: Optional[str] = None
    tiene_resultados: bool = False

    class Config:
        from_attributes = True
