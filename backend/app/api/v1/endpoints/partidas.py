from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.deps import get_db
from app.services.partida_service import PartidaService

router = APIRouter()

@router.post("/iniciar/{campeonato_id}")
def iniciar_partida(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Iniciar una nueva partida en el campeonato.
    """
    return PartidaService(db).iniciar_partida(campeonato_id)

@router.post("/finalizar/{campeonato_id}")
def finalizar_partida(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Finalizar la partida actual del campeonato.
    """
    return PartidaService(db).finalizar_partida(campeonato_id)

@router.get("/verificar-completa/{campeonato_id}/{partida}")
def verificar_partida_completa(
    campeonato_id: int,
    partida: int,
    db: Session = Depends(get_db)
):
    """
    Verificar si todos los resultados de una partida están registrados.
    """
    return {
        "completa": PartidaService(db).verificar_partida_completa(
            campeonato_id,
            partida
        )
    }

@router.get("/mesas-asignadas/{campeonato_id}")
def get_mesas_asignadas(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener las mesas asignadas para la partida actual.
    """
    return PartidaService(db).get_mesas_asignadas(campeonato_id)

@router.post("/sortear-parejas/{campeonato_id}")
def sortear_parejas(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Realizar el sorteo de parejas para una nueva partida.
    """
    return PartidaService(db).sortear_parejas(campeonato_id) 