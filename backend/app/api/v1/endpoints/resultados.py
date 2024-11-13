from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.resultado import ResultadoCreate, ResultadoResponse, ResultadoRanking
from app.services.resultado_service import ResultadoService

router = APIRouter()

@router.post("/", response_model=ResultadoResponse)
def create_resultado(
    resultado: ResultadoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo resultado.
    """
    return ResultadoService(db).create_resultado(resultado)

@router.get("/{mesa_id}/{partida}", response_model=ResultadoResponse)
def get_resultados(
    mesa_id: int,
    partida: int,
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener resultados de una mesa específica.
    """
    return ResultadoService(db).get_resultados(mesa_id, partida, campeonato_id)

@router.get("/campeonato/{campeonato_id}", response_model=List[ResultadoRanking])
def get_ranking_campeonato(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener el ranking actual del campeonato.
    """
    return ResultadoService(db).get_ranking_campeonato(campeonato_id)

@router.post("/ajustar-pg")
def ajustar_pg(
    campeonato_id: int,
    pareja_id: int,
    nuevo_pg: int,
    db: Session = Depends(get_db)
):
    """
    Ajustar los PG de una pareja en la última partida.
    """
    return ResultadoService(db).ajustar_pg(campeonato_id, pareja_id, nuevo_pg)

@router.get("/verificar-ultima-partida/{pareja1_id}/{pareja2_id}")
def verificar_ultima_partida(
    pareja1_id: int,
    pareja2_id: int,
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Verificar si dos parejas pueden jugar juntas basado en sus últimos resultados.
    """
    return ResultadoService(db).verificar_ultima_partida(
        campeonato_id,
        pareja1_id,
        pareja2_id
    )

@router.post("/actualizar-gb")
def actualizar_gb(
    campeonato_id: int,
    pareja_id: int,
    gb: str,
    partida_actual: int,
    db: Session = Depends(get_db)
):
    """
    Actualizar el grupo (A/B) de una pareja.
    """
    return ResultadoService(db).actualizar_gb(
        campeonato_id,
        pareja_id,
        gb,
        partida_actual
    )
