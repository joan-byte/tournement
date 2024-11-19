from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Campeonato, Pareja, Mesa, Resultado
from typing import List
from sqlalchemy import and_
import random

router = APIRouter()

@router.get("/{campeonato_id}/mesas")
async def get_mesas_partida(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Obtiene las mesas asignadas para la partida actual del campeonato
    """
    try:
        # Obtener el campeonato y su partida actual
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Obtener las mesas de la partida actual
        mesas = db.query(Mesa).filter(
            and_(
                Mesa.campeonato_id == campeonato_id,
                Mesa.partida == campeonato.partida_actual
            )
        ).all()

        # Si no hay mesas, devolver lista vacía
        if not mesas:
            return []

        # Cargar las parejas relacionadas
        for mesa in mesas:
            mesa.pareja1 = db.query(Pareja).filter(Pareja.id == mesa.pareja1_id).first()
            if mesa.pareja2_id:
                mesa.pareja2 = db.query(Pareja).filter(Pareja.id == mesa.pareja2_id).first()

            # Verificar si la mesa tiene resultados
            resultado = db.query(Resultado).filter(
                and_(
                    Resultado.mesa_id == mesa.id,
                    Resultado.partida == campeonato.partida_actual
                )
            ).first()
            mesa.tieneResultado = resultado is not None

        return mesas

    except Exception as e:
        print(f"Error obteniendo mesas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener las mesas: {str(e)}"
        )

@router.post("/sortear-parejas/{campeonato_id}")
async def sortear_parejas(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # 1. Obtener el ranking actual
        resultados = db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id
        ).order_by(Resultado.PG.desc(), Resultado.PP.desc()).all()

        # 2. Obtener todas las parejas activas
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        # 3. Ordenar parejas
        if resultados:
            # Si hay resultados previos, ordenar según ranking
            parejas_ordenadas = sorted(
                parejas,
                key=lambda p: next(
                    (r.PG * 1000 + r.PP for r in resultados if r.id_pareja == p.id),
                    0
                ),
                reverse=True
            )
        else:
            # Para la primera partida, hacer sorteo aleatorio
            parejas_ordenadas = list(parejas)  # Crear una copia de la lista
            random.shuffle(parejas_ordenadas)  # Mezclar aleatoriamente

        # 4. Emparejar las parejas (1 vs 2, 3 vs 4, etc.)
        parejas_emparejadas = []
        for i in range(0, len(parejas_ordenadas), 2):
            if i + 1 < len(parejas_ordenadas):
                parejas_emparejadas.append((parejas_ordenadas[i], parejas_ordenadas[i + 1]))
            else:
                parejas_emparejadas.append((parejas_ordenadas[i], None))

        # 5. Obtener la partida actual del campeonato
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # 6. Crear las mesas (siempre con partida = 1 al cerrar inscripción)
        for mesa_num, (pareja1, pareja2) in enumerate(parejas_emparejadas, 1):
            mesa = Mesa(
                numero=mesa_num,
                campeonato_id=campeonato_id,
                partida=1,
                pareja1_id=pareja1.id,
                pareja2_id=pareja2.id if pareja2 else None
            )
            db.add(mesa)

        db.commit()
        return {"message": "Mesas asignadas correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al sortear parejas: {str(e)}"
        )

@router.delete("/{campeonato_id}/mesas")
async def eliminar_mesas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Eliminar todas las mesas del campeonato sin importar la partida
        db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id
        ).delete()
        
        db.commit()
        return {"message": "Mesas eliminadas correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))