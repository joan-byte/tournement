from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.models.campeonato import Campeonato
from app.models.resultado import Resultado
import random

router = APIRouter()

@router.get("/")
def get_partidas(db: Session = Depends(get_db)):
    return {"message": "Lista de partidas"}

@router.post("/{campeonato_id}/sorteo-inicial")
def realizar_sorteo_inicial(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Verificar que el campeonato existe
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

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

        # Actualizar el número de partida en el campeonato
        campeonato.partida_actual = 1
        
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
def get_mesas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Primero obtener el campeonato para saber la partida actual
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Obtener las mesas de la partida actual
        mesas = db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id,
            Mesa.partida == campeonato.partida_actual
        ).order_by(Mesa.numero).all()

        # Verificar si cada mesa tiene resultados registrados
        response = []
        for mesa in mesas:
            resultados = db.query(Resultado).filter(
                Resultado.mesa_id == mesa.id,
                Resultado.partida == campeonato.partida_actual
            ).count()

            mesa_data = {
                "id": mesa.id,
                "numero": mesa.numero,
                "pareja1": {
                    "id": mesa.pareja1.id,
                    "numero": mesa.pareja1.numero,
                    "nombre": mesa.pareja1.nombre,
                    "club": mesa.pareja1.club
                } if mesa.pareja1 else None,
                "pareja2": {
                    "id": mesa.pareja2.id,
                    "numero": mesa.pareja2.numero,
                    "nombre": mesa.pareja2.nombre,
                    "club": mesa.pareja2.club
                } if mesa.pareja2 else None,
                "tieneResultado": resultados > 0
            }
            response.append(mesa_data)

        return response

    except Exception as e:
        print(f"Error obteniendo mesas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mesa/{mesa_id}")
def get_mesa(mesa_id: int, db: Session = Depends(get_db)):
    try:
        mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")
            
        return {
            "id": mesa.id,
            "numero": mesa.numero,
            "pareja1": {
                "id": mesa.pareja1.id,
                "numero": mesa.pareja1.numero,
                "nombre": mesa.pareja1.nombre
            } if mesa.pareja1 else None,
            "pareja2": {
                "id": mesa.pareja2.id,
                "numero": mesa.pareja2.numero,
                "nombre": mesa.pareja2.nombre
            } if mesa.pareja2 else None,
            "tieneResultado": bool(mesa.resultados)
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{campeonato_id}/cerrar-partida")
def cerrar_partida(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Verificar que el campeonato existe
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Verificar que todas las mesas tienen resultados para la partida actual
        mesas_actuales = db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id,
            Mesa.partida == campeonato.partida_actual
        ).all()

        for mesa in mesas_actuales:
            resultados = db.query(Resultado).filter(
                Resultado.mesa_id == mesa.id,
                Resultado.partida == campeonato.partida_actual
            ).count()
            if resultados == 0:
                raise HTTPException(
                    status_code=400, 
                    detail=f"La mesa {mesa.numero} no tiene resultados registrados"
                )

        # Obtener ranking actual
        ranking = db.query(
            Pareja.id,
            func.sum(Resultado.PG).label('total_pg'),
            func.sum(Resultado.PP).label('total_pp')
        ).join(
            Resultado, Resultado.id_pareja == Pareja.id
        ).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).group_by(
            Pareja.id
        ).order_by(
            func.sum(Resultado.PG).desc(),
            func.sum(Resultado.PP).desc()
        ).all()

        # Crear lista ordenada de parejas
        parejas_ordenadas = [p.id for p in ranking]

        # Crear nuevas mesas para la siguiente partida
        nueva_partida = campeonato.partida_actual + 1
        for i in range(0, len(parejas_ordenadas), 2):
            pareja1_id = parejas_ordenadas[i]
            pareja2_id = parejas_ordenadas[i + 1] if i + 1 < len(parejas_ordenadas) else None
            
            mesa = Mesa(
                numero=i//2 + 1,
                campeonato_id=campeonato_id,
                partida=nueva_partida,  # Asignar a la nueva partida
                pareja1_id=pareja1_id,
                pareja2_id=pareja2_id
            )
            db.add(mesa)

        # Incrementar partida actual
        campeonato.partida_actual = nueva_partida

        db.commit()
        return {"message": "Partida cerrada y nueva distribución creada"}
            
    except Exception as e:
        db.rollback()
        print(f"Error cerrando partida: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ranking/{campeonato_id}")
def get_ranking(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener ranking actual con la última partida jugada
        ranking = db.query(
            Pareja.id,
            Pareja.numero,
            Pareja.nombre,
            Pareja.club,
            func.sum(Resultado.PG).label('total_pg'),
            func.sum(Resultado.PP).label('total_pp'),
            func.max(Resultado.partida).label('ultima_partida')  # Añadido este campo
        ).join(
            Resultado, Resultado.id_pareja == Pareja.id
        ).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).group_by(
            Pareja.id,
            Pareja.numero,
            Pareja.nombre,
            Pareja.club
        ).order_by(
            func.sum(Resultado.PG).desc(),
            func.sum(Resultado.PP).desc()
        ).all()

        # Formatear resultados
        response = []
        for idx, r in enumerate(ranking, 1):
            response.append({
                "posicion": idx,
                "pareja_id": r.id,
                "numero": r.numero,
                "nombre": r.nombre,
                "club": r.club,
                "GB": "A",  # Por ahora siempre es A
                "PG": int(r.total_pg or 0),
                "PP": int(r.total_pp or 0),
                "ultima_partida": int(r.ultima_partida or 0)  # Incluido en la respuesta
            })

        return response

    except Exception as e:
        print(f"Error obteniendo ranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))