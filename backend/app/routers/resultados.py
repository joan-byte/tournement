from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.models.campeonato import Campeonato
from typing import List, Dict, Any
from app.schemas.resultado import RankingResultado

router = APIRouter()

@router.get("/ranking/{campeonato_id}", response_model=List[RankingResultado])
def get_ranking(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el ranking actual del campeonato.
    
    Args:
        campeonato_id: ID del campeonato
        db: Sesión de la base de datos
    
    Returns:
        Lista ordenada de parejas con sus estadísticas actuales
    
    Note:
        Solo incluye parejas activas y con resultados reales (no iniciales)
    """
    try:
        # Obtener todas las parejas activas del campeonato
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        if not parejas:
            return []

        # Obtener solo resultados con valores reales (no iniciales)
        # Se filtran resultados donde al menos uno de los valores sea diferente de 0
        resultados = db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            (Resultado.PG != 0) | (Resultado.PP != 0) | (Resultado.RP != 0)
        ).all()

        if not resultados:
            return []

        # Construir el ranking procesando cada pareja
        ranking = []
        for pareja in parejas:
            # Filtrar resultados específicos de esta pareja
            resultados_pareja = [r for r in resultados if r.id_pareja == pareja.id]
            
            if resultados_pareja:  # Solo incluir parejas con resultados reales
                # Calcular estadísticas acumuladas
                total_pg = sum(1 for r in resultados_pareja if r.PG == 1)
                total_pp = sum(r.PP for r in resultados_pareja)
                ultima_partida = max([r.partida for r in resultados_pareja])

                # Crear item del ranking con todos los datos necesarios
                ranking_item = RankingResultado(
                    posicion=0,  # Se actualizará después de ordenar
                    GB='A',      # Grupo A por defecto
                    PG=total_pg, # Partidas ganadas
                    PP=total_pp, # Puntos perdidos
                    ultima_partida=ultima_partida,
                    numero=pareja.numero,
                    nombre=pareja.nombre,
                    pareja_id=pareja.id,
                    club=pareja.club
                )
                ranking.append(ranking_item)

        # Ordenar el ranking según los criterios establecidos
        # Primero por GB, luego por PG (descendente) y PP (descendente)
        ranking.sort(key=lambda x: (x.GB, -x.PG, -x.PP))

        # Asignar posiciones después de ordenar
        for idx, item in enumerate(ranking, 1):
            item.posicion = idx

        # Agregar este log antes del return
        print("Respuesta del backend:", ranking)
        return ranking

    except Exception as e:
        print(f"Error obteniendo ranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{mesa_id}/{partida}")
def get_resultado_mesa(mesa_id: int, partida: int, db: Session = Depends(get_db)):
    """
    Obtiene los resultados de una mesa específica en una partida.
    
    Args:
        mesa_id: ID de la mesa
        partida: Número de la partida
        db: Sesión de la base de datos
    
    Returns:
        Diccionario con los resultados de ambas parejas o None si no hay resultados
    """
    try:
        # Verificar que la mesa existe
        mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Obtener resultados de la mesa para la partida específica
        resultados = db.query(Resultado).filter(
            Resultado.mesa_id == mesa_id,
            Resultado.partida == partida
        ).all()
        
        if not resultados:
            return None
            
        # Formatear la respuesta separando resultados por pareja
        response = {
            "pareja1": next((r.to_dict() for r in resultados if r.id_pareja == mesa.pareja1_id), None),
            "pareja2": next((r.to_dict() for r in resultados if r.id_pareja == mesa.pareja2_id), None) if mesa.pareja2_id else None
        }
        
        return response
            
    except Exception as e:
        print(f"Error en get_resultado_mesa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def save_resultado(data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Guarda los resultados de una partida.
    
    Args:
        data: Diccionario con los datos del resultado
        db: Sesión de la base de datos
    
    Returns:
        Mensaje de confirmación
    
    Note:
        - Requiere mesa_id, campeonato_id y datos de al menos la pareja1
        - Maneja automáticamente la eliminación de resultados previos
    """
    try:
        # Validar que estén todos los campos requeridos
        if not all(key in data for key in ['mesa_id', 'campeonato_id', 'pareja1']):
            raise HTTPException(status_code=400, detail="Faltan campos requeridos")

        # Verificar que la mesa existe
        mesa = db.query(Mesa).filter(Mesa.id == data['mesa_id']).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Obtener el campeonato para la partida actual
        campeonato = db.query(Campeonato).filter(
            Campeonato.id == data['campeonato_id']
        ).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Eliminar resultados previos si existen
        db.query(Resultado).filter(
            Resultado.mesa_id == data['mesa_id'],
            Resultado.partida == campeonato.partida_actual
        ).delete()

        # Guardar resultado de la primera pareja
        resultado1 = Resultado(
            mesa_id=data['mesa_id'],
            campeonato_id=data['campeonato_id'],
            partida=campeonato.partida_actual,
            id_pareja=mesa.pareja1_id,
            GB='A',
            RP=data['pareja1']['RP'],
            PP=data['pareja1']['PP'],
            PG=data['pareja1']['PG']
        )
        db.add(resultado1)

        # Guardar resultado de la segunda pareja si existe
        if mesa.pareja2_id and 'pareja2' in data:
            resultado2 = Resultado(
                mesa_id=data['mesa_id'],
                campeonato_id=data['campeonato_id'],
                partida=campeonato.partida_actual,
                id_pareja=mesa.pareja2_id,
                GB='A',
                RP=data['pareja2']['RP'],
                PP=data['pareja2']['PP'],
                PG=data['pareja2']['PG']
            )
            db.add(resultado2)

        db.commit()
        return {"message": "Resultados guardados correctamente"}

    except Exception as e:
        db.rollback()
        print(f"Error guardando resultado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))