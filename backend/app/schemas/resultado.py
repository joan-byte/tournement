from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoBase(BaseModel):
    campeonato_id: int
    P: int  # Partida
    M: int  # Mesa
    id_pareja: int
    RP: int  # Resultado Parcial
    PG: int  # Puntos Ganados
    PP: int  # Puntos Perdidos
    GB: str  # Grupo (A/B)

class ResultadoPareja(BaseModel):
    P: int
    M: int
    id_pareja: int
    RP: int
    PG: int
    PP: int
    GB: str

class ResultadoCreate(BaseModel):
    campeonato_id: int
    pareja1: ResultadoPareja
    pareja2: Optional[ResultadoPareja] = None

class ResultadoUpdate(ResultadoCreate):
    pass

class ResultadoInDB(ResultadoBase):
    id: int

    class Config:
        from_attributes = True

class ResultadoResponse(BaseModel):
    pareja1: Optional[ResultadoInDB]
    pareja2: Optional[ResultadoInDB] = None

    class Config:
        from_attributes = True

class ResultadoRanking(BaseModel):
    pareja_id: int
    nombre_pareja: str
    club: Optional[str]
    PG: int
    PP: int
    GB: str
    posicion: Optional[int] = None

    class Config:
        from_attributes = True

class ResultadoHistorico(ResultadoBase):
    fecha: datetime
    mesa_numero: int
    rival_nombre: Optional[str]
    rival_resultado: Optional[int]

    class Config:
        from_attributes = True

class RankingFinal(BaseModel):
    pareja_id: int
    nombre_pareja: str
    club: Optional[str]
    PG_total: int
    PP_total: int
    GB_final: str
    posicion_final: int
    premio: Optional[str]

    class Config:
        from_attributes = True

class ResultadoEstadisticas(BaseModel):
    total_partidas: int
    victorias: int
    derrotas: int
    promedio_PP: float
    mejor_resultado: int
    peor_resultado: int
    resultados_por_grupo: dict[str, int]  # {'A': count, 'B': count}

    class Config:
        from_attributes = True
