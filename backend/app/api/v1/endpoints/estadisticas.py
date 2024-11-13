from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.estadisticas_service import EstadisticasService
from app.schemas.resultado import ResultadoEstadisticas

router = APIRouter()

@router.get("/pareja/{pareja_id}", response_model=ResultadoEstadisticas)
def get_estadisticas_pareja(
    pareja_id: int,
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas de una pareja en un campeonato.
    """
    return EstadisticasService(db).get_estadisticas_pareja(pareja_id, campeonato_id) 