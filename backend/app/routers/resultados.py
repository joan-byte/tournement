from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.resultado_service import ResultadoService
from app.schemas.resultado import ResultadoCreate, ResultadoResponse
from typing import List

router = APIRouter()

@router.get("/ranking/{campeonato_id}")
def get_ranking(campeonato_id: int, db: Session = Depends(get_db)) -> List[dict]:
    resultado_service = ResultadoService(db)
    return resultado_service.obtener_ranking(campeonato_id)

@router.post("/")
def create_resultado(resultado: ResultadoCreate, db: Session = Depends(get_db)) -> ResultadoResponse:
    resultado_service = ResultadoService(db)
    return resultado_service.create_resultado(resultado)

# ... resto de los endpoints ...