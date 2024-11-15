from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.pareja import Pareja
from app.schemas.pareja import ParejaCreate, ParejaUpdate

router = APIRouter()

@router.get("/campeonato/{campeonato_id}")
def get_parejas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    return db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).all()

# ... resto de endpoints ... 