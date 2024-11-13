from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.services.historial_service import HistorialService
from app.schemas.resultado import ResultadoHistorico

router = APIRouter()

@router.get("/pareja/{pareja_id}", response_model=List[ResultadoHistorico])
def get_historial_pareja(
    pareja_id: int,
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener historial de resultados de una pareja.
    """
    return HistorialService(db).get_historial_pareja(pareja_id, campeonato_id) 