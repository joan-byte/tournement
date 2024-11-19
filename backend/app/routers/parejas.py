from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.pareja import Pareja
from app.models.jugador import Jugador
from app.schemas.pareja import ParejaCreate, ParejaUpdate
from typing import Dict, List

router = APIRouter()

@router.get("/campeonato/{campeonato_id}")
def get_parejas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener todas las parejas del campeonato
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id
        ).all()
        
        # Log para debugging
        print(f"Parejas encontradas para campeonato {campeonato_id}: {len(parejas)}")
        return parejas
    except Exception as e:
        print(f"Error al obtener parejas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener parejas: {str(e)}"
        )

@router.post("/")
async def create_pareja(pareja_data: Dict, db: Session = Depends(get_db)):
    try:
        # Crear la pareja
        nueva_pareja = Pareja(
            nombre=f"{pareja_data['jugador1']['nombre']} {pareja_data['jugador1']['apellido']} Y {pareja_data['jugador2']['nombre']} {pareja_data['jugador2']['apellido']}",
            club=pareja_data.get('club', ''),
            activa=True,
            campeonato_id=pareja_data['campeonato_id']
        )

        # Obtener el último número de pareja para este campeonato
        ultima_pareja = db.query(Pareja)\
            .filter(Pareja.campeonato_id == pareja_data['campeonato_id'])\
            .order_by(Pareja.numero.desc())\
            .first()
        
        nueva_pareja.numero = 1 if not ultima_pareja else ultima_pareja.numero + 1
        
        db.add(nueva_pareja)
        db.flush()  # Para obtener el ID de la pareja

        # Crear los jugadores
        jugador1 = Jugador(
            nombre=pareja_data['jugador1']['nombre'],
            apellido=pareja_data['jugador1']['apellido'],
            pareja_id=nueva_pareja.id,
            campeonato_id=pareja_data['campeonato_id']
        )

        jugador2 = Jugador(
            nombre=pareja_data['jugador2']['nombre'],
            apellido=pareja_data['jugador2']['apellido'],
            pareja_id=nueva_pareja.id,
            campeonato_id=pareja_data['campeonato_id']
        )

        db.add(jugador1)
        db.add(jugador2)
        
        db.commit()
        db.refresh(nueva_pareja)
        
        return nueva_pareja

    except Exception as e:
        db.rollback()
        print(f"Error al crear pareja: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear pareja: {str(e)}"
        )

@router.put("/{pareja_id}")
async def update_pareja(
    pareja_id: int,
    update_data: Dict,
    db: Session = Depends(get_db)
):
    try:
        # Buscar la pareja
        pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
        if not pareja:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pareja no encontrada"
            )

        # Actualizar solo los campos proporcionados
        for key, value in update_data.items():
            if hasattr(pareja, key):
                setattr(pareja, key, value)

        db.commit()
        db.refresh(pareja)
        return pareja

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la pareja: {str(e)}"
        )

# ... resto de endpoints ... 