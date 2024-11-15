from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Mesa, Pareja

router = APIRouter()

@router.get("/")
def get_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).all()

@router.get("/{mesa_id}")
async def get_mesa(mesa_id: int, db: Session = Depends(get_db)):
    try:
        mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Cargar las parejas relacionadas
        mesa.pareja1 = db.query(Pareja).filter(Pareja.id == mesa.pareja1_id).first()
        if mesa.pareja2_id:
            mesa.pareja2 = db.query(Pareja).filter(Pareja.id == mesa.pareja2_id).first()

        return mesa
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener la mesa: {str(e)}"
        ) 