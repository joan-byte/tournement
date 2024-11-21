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
    Obtiene las mesas asignadas para la partida actual del campeonato.
    
    Args:
        campeonato_id: ID del campeonato
        db: Sesión de la base de datos
    
    Returns:
        Lista de mesas con información detallada de las parejas y resultados
    
    Raises:
        HTTPException: Si hay error al obtener las mesas o no se encuentra el campeonato
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
        ).order_by(Mesa.numero).all()

        # Si no hay mesas, devolver lista vacía
        if not mesas:
            return []

        # Cargar las parejas relacionadas y construir respuesta detallada
        mesas_con_parejas = []
        for mesa in mesas:
            # Verificar si hay resultados para esta mesa
            resultado_existente = db.query(Resultado).filter(
                Resultado.mesa_id == mesa.id,
                Resultado.partida == campeonato.partida_actual
            ).first()

            # Obtener pareja1
            pareja1 = db.query(Pareja).filter(Pareja.id == mesa.pareja1_id).first()
            # Obtener pareja2 si existe
            pareja2 = None
            if mesa.pareja2_id:
                pareja2 = db.query(Pareja).filter(Pareja.id == mesa.pareja2_id).first()

            # Crear diccionario con toda la información
            mesa_dict = {
                "id": mesa.id,
                "numero": mesa.numero,
                "campeonato_id": mesa.campeonato_id,
                "partida": mesa.partida,
                "tieneResultado": resultado_existente is not None,
                "pareja1": {
                    "id": pareja1.id,
                    "numero": pareja1.numero,
                    "nombre": pareja1.nombre,
                    "club": pareja1.club
                } if pareja1 else None,
                "pareja2": {
                    "id": pareja2.id,
                    "numero": pareja2.numero,
                    "nombre": pareja2.nombre,
                    "club": pareja2.club
                } if pareja2 else None
            }
            mesas_con_parejas.append(mesa_dict)

        return mesas_con_parejas

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener las mesas: {str(e)}"
        )

@router.post("/sortear-parejas/{campeonato_id}")
async def sortear_parejas(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Realiza el sorteo de parejas para una nueva partida.
    
    Args:
        campeonato_id: ID del campeonato
        db: Sesión de la base de datos
    
    Returns:
        Mensaje de confirmación del sorteo
    
    Note:
        - Para la primera partida realiza un sorteo aleatorio
        - Para partidas posteriores ordena por ranking
    """
    try:
        # Obtener el campeonato
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # 1. Obtener todas las parejas activas
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        # 2. Verificar si hay resultados previos para determinar si es la primera partida
        resultados_previos = db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            (Resultado.PG != 0) | (Resultado.PP != 0) | (Resultado.RP != 0)
        ).first()

        # Si no hay resultados previos, hacer sorteo aleatorio
        if not resultados_previos:
            print("Primera partida: realizando sorteo aleatorio")
            parejas_ordenadas = list(parejas)
            random.shuffle(parejas_ordenadas)
        else:
            print("Partida posterior: ordenando por ranking")
            # Para siguientes partidas, ordenar por ranking
            resultados = db.query(Resultado).filter(
                Resultado.campeonato_id == campeonato_id
            ).order_by(Resultado.PG.desc(), Resultado.PP.desc()).all()
            
            parejas_ordenadas = sorted(
                parejas,
                key=lambda p: next(
                    (r.PG * 1000 + r.PP for r in resultados if r.id_pareja == p.id),
                    0
                ),
                reverse=True
            )

        # 3. Emparejar las parejas
        parejas_emparejadas = []
        for i in range(0, len(parejas_ordenadas), 2):
            if i + 1 < len(parejas_ordenadas):
                parejas_emparejadas.append((parejas_ordenadas[i], parejas_ordenadas[i + 1]))
            else:
                parejas_emparejadas.append((parejas_ordenadas[i], None))

        # 4. Crear las mesas para la partida correspondiente
        partida_destino = campeonato.partida_actual
        
        for mesa_num, (pareja1, pareja2) in enumerate(parejas_emparejadas, 1):
            mesa = Mesa(
                numero=mesa_num,
                campeonato_id=campeonato_id,
                partida=partida_destino,
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
    """
    Elimina todas las mesas de un campeonato específico.
    
    Args:
        campeonato_id: ID del campeonato
        db: Sesión de la base de datos
    
    Returns:
        Mensaje de confirmación de la eliminación
    
    Note:
        Realiza una eliminación segura verificando que todas las mesas
        se hayan eliminado correctamente
    """
    try:
        # Primero obtener todas las mesas del campeonato
        mesas = db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).all()
        
        if not mesas:
            return {"message": "No hay mesas para eliminar"}

        # Eliminar cada mesa individualmente para asegurar que se eliminan todas
        for mesa in mesas:
            db.delete(mesa)
        
        # Hacer commit de los cambios
        db.commit()
        
        # Verificar que se eliminaron todas las mesas
        mesas_restantes = db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).count()
        if mesas_restantes > 0:
            raise HTTPException(
                status_code=500,
                detail="No se pudieron eliminar todas las mesas"
            )
            
        return {"message": "Mesas eliminadas correctamente"}
    except Exception as e:
        db.rollback()
        print(f"Error eliminando mesas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))