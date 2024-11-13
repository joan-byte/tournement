from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.deps import get_db
from app.services.ranking_service import RankingService

router = APIRouter()

@router.get("/{campeonato_id}")
def get_ranking(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener el ranking actual del campeonato.
    """
    return RankingService(db).get_ranking(campeonato_id)

@router.get("/{campeonato_id}/final")
def get_ranking_final(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener el ranking final del campeonato.
    """
    return RankingService(db).get_ranking_final(campeonato_id)

@router.post("/{campeonato_id}/actualizar")
def actualizar_ranking(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Actualizar el ranking del campeonato.
    """
    return RankingService(db).actualizar_ranking(campeonato_id)

@router.get("/{campeonato_id}/grupo/{grupo}")
def get_ranking_por_grupo(
    campeonato_id: int,
    grupo: str,
    db: Session = Depends(get_db)
):
    """
    Obtener el ranking filtrado por grupo (A/B).
    """
    return RankingService(db).get_ranking_por_grupo(campeonato_id, grupo)

@router.get("/{campeonato_id}/pareja/{pareja_id}")
def get_ranking_pareja(
    campeonato_id: int,
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener el historial de resultados de una pareja específica.
    """
    return RankingService(db).get_ranking_pareja(campeonato_id, pareja_id) 