from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.mesa import Mesa
from app.models.pareja import Pareja
import random

router = APIRouter()

@router.get("/")
def get_partidas(db: Session = Depends(get_db)):
    return {"message": "Lista de partidas"}

@router.post("/{campeonato_id}/sorteo-inicial")
def realizar_sorteo_inicial(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener solo las parejas activas
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()
        
        if len(parejas) < 4:
            raise HTTPException(
                status_code=400, 
                detail="Se necesitan al menos 4 parejas activas para iniciar el campeonato"
            )

        # Mezclar las parejas aleatoriamente
        parejas_mezcladas = random.sample(parejas, len(parejas))
        
        # Crear las mesas
        mesas = []
        for i in range(0, len(parejas_mezcladas), 2):
            pareja1 = parejas_mezcladas[i]
            pareja2 = parejas_mezcladas[i + 1] if i + 1 < len(parejas_mezcladas) else None
            
            mesa = Mesa(
                numero=i//2 + 1,  # Numeración de mesas empezando en 1
                campeonato_id=campeonato_id,
                partida=1,  # Primera partida
                pareja1_id=pareja1.id,
                pareja2_id=pareja2.id if pareja2 else None
            )
            mesas.append(mesa)
        
        # Guardar las mesas en la base de datos
        for mesa in mesas:
            db.add(mesa)
        
        db.commit()
        return {"message": "Sorteo realizado con éxito", "mesas": len(mesas)}
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 

@router.delete("/{campeonato_id}/mesas")
def eliminar_mesas(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Eliminar todas las mesas del campeonato
        db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).delete()
        db.commit()
        return {"message": "Mesas eliminadas correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/{campeonato_id}/mesas")
def get_mesas_asignadas(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener todas las mesas del campeonato con sus parejas
        mesas = db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id
        ).all()
        
        # Preparar la lista de parejas con sus mesas asignadas
        parejas_mesas = []
        for mesa in mesas:
            if mesa.pareja1:
                parejas_mesas.append({
                    "id": mesa.pareja1.id,
                    "numero": mesa.pareja1.numero,
                    "nombre": mesa.pareja1.nombre,
                    "club": mesa.pareja1.club,
                    "mesa_numero": mesa.numero
                })
            if mesa.pareja2:
                parejas_mesas.append({
                    "id": mesa.pareja2.id,
                    "numero": mesa.pareja2.numero,
                    "nombre": mesa.pareja2.nombre,
                    "club": mesa.pareja2.club,
                    "mesa_numero": mesa.numero
                })
        
        return parejas_mesas
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))