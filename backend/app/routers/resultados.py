from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.resultado import Resultado

router = APIRouter()

@router.get("/")
def get_resultados(db: Session = Depends(get_db)):
    return db.query(Resultado).all()

@router.get("/{mesa_id}/{partida}")
def get_resultado_mesa(
    mesa_id: int,
    partida: int,
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    resultado = db.query(Resultado).filter(
        Resultado.mesa_id == mesa_id,
        Resultado.partida == partida,
        Resultado.campeonato_id == campeonato_id
    ).first()
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado 