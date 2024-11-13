from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.mesa import Mesa
from app.models.pareja import Pareja

router = APIRouter()

@router.get("/")
def get_partidas(db: Session = Depends(get_db)):
    return {"message": "Lista de partidas"}

@router.post("/{campeonato_id}/sorteo-inicial")
def realizar_sorteo_inicial(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()
        
        if not parejas:
            raise HTTPException(status_code=400, detail="No hay parejas activas")
            
        return {"message": "Sorteo realizado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 