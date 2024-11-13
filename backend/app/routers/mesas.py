from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.mesa import Mesa

router = APIRouter()

@router.get("/")
def get_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).all()

@router.get("/{mesa_id}")
def get_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa 