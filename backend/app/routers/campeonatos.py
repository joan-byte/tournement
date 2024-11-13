from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.campeonato import Campeonato
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate
from datetime import date

router = APIRouter()

@router.get("/")
def get_campeonatos(db: Session = Depends(get_db)):
    return db.query(Campeonato).all()

@router.get("/{campeonato_id}")
def get_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    return campeonato

@router.post("/")
async def create_campeonato(campeonato: CampeonatoCreate, db: Session = Depends(get_db)):
    try:
        db_campeonato = Campeonato(
            nombre=campeonato.nombre,
            fecha_inicio=campeonato.fecha_inicio,
            dias_duracion=campeonato.dias_duracion,
            numero_partidas=campeonato.numero_partidas,
            grupo_b=campeonato.grupo_b,
            partida_actual=0
        )
        db.add(db_campeonato)
        db.commit()
        db.refresh(db_campeonato)
        return db_campeonato
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{campeonato_id}")
def update_campeonato(
    campeonato_id: int, 
    campeonato_data: CampeonatoUpdate,
    db: Session = Depends(get_db)
):
    campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    
    for key, value in campeonato_data.dict(exclude_unset=True).items():
        setattr(campeonato, key, value)
    
    db.commit()
    db.refresh(campeonato)
    return campeonato 