from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.campeonato import Campeonato
from app.models.pareja import Pareja
from app.models.jugador import Jugador
from app.models.mesa import Mesa
from app.models.resultado import Resultado
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate
from datetime import date

router = APIRouter()

@router.get("/")
def get_campeonatos(db: Session = Depends(get_db)):
    return db.query(Campeonato).all()

@router.get("/{campeonato_id}")
def get_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        # Forzar la carga de los datos antes de devolver
        db.refresh(campeonato)
        
        # Log para depuración
        print(f"Devolviendo campeonato: {campeonato.id} - {campeonato.nombre}")
        
        return campeonato
    except Exception as e:
        print(f"Error al obtener campeonato: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        for key, value in campeonato_data.dict(exclude_unset=True).items():
            setattr(campeonato, key, value)
        
        db.commit()
        db.refresh(campeonato)
        
        # Log para depuración
        print(f"Campeonato actualizado: {campeonato.id} - {campeonato.nombre}")
        
        return campeonato
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar campeonato: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{campeonato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Elimina un campeonato y todos sus datos relacionados
    """
    try:
        # Primero verificamos que el campeonato existe
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campeonato no encontrado"
            )

        # Eliminamos todos los datos relacionados en orden
        # 1. Resultados
        db.query(Resultado).filter(Resultado.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 2. Mesas
        db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 3. Jugadores
        db.query(Jugador).filter(Jugador.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 4. Parejas
        db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).delete(synchronize_session=False)
        
        # 5. Finalmente, el campeonato
        db.query(Campeonato).filter(Campeonato.id == campeonato_id).delete(synchronize_session=False)
        
        # Confirmamos los cambios
        db.commit()
        
        return {"message": "Campeonato eliminado correctamente"}
        
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar campeonato: {str(e)}")  # Para debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el campeonato: {str(e)}"
        ) 