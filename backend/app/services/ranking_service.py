from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.resultado import Resultado
from app.models.pareja import Pareja
from app.models.campeonato import Campeonato
from sqlalchemy import func, case
from typing import List, Dict, Any

class RankingService:
    """
    Servicio que maneja todas las operaciones relacionadas con el ranking del campeonato.
    Proporciona funcionalidad para calcular y consultar diferentes tipos de rankings.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de ranking.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_ranking(self, campeonato_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el ranking actual del campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de diccionarios con las estadísticas de cada pareja,
            ordenada por PG (descendente) y PP (ascendente)
            
        Raises:
            HTTPException: Si el campeonato no existe
            
        Note:
            Incluye PG (Partidas Ganadas), PP (Puntos Perdidos) y GB (Grupo)
        """
        # Verificar que el campeonato existe
        campeonato = self.db.query(Campeonato).filter(
            Campeonato.id == campeonato_id
        ).first()
        if not campeonato:
            raise HTTPException(
                status_code=404,
                detail="Campeonato no encontrado"
            )

        # Obtener los resultados agrupados por pareja
        # Calcula totales de PG, PP y determina el grupo (A/B)
        resultados = self.db.query(
            Resultado.id_pareja,
            Pareja.nombre.label('nombre_pareja'),
            Pareja.club,
            func.sum(Resultado.PG).label('total_PG'),
            func.sum(Resultado.PP).label('total_PP'),
            func.max(case(
                (Resultado.GB == 'B', 'B'),
                else_='A'
            )).label('GB')
        ).join(
            Pareja,
            Resultado.id_pareja == Pareja.id
        ).filter(
            Resultado.campeonato_id == campeonato_id
        ).group_by(
            Resultado.id_pareja,
            Pareja.nombre,
            Pareja.club
        ).all()

        # Convertir los resultados a diccionarios y ordenarlos
        ranking = [
            {
                'pareja_id': r.id_pareja,
                'nombre_pareja': r.nombre_pareja,
                'club': r.club,
                'PG': r.total_PG,
                'PP': r.total_PP,
                'GB': r.GB
            }
            for r in resultados
        ]
        
        # Ordenar por PG (descendente) y PP (ascendente)
        ranking.sort(key=lambda x: (-x['PG'], x['PP']))
        return ranking

    def get_ranking_final(self, campeonato_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el ranking final del campeonato una vez finalizado.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista ordenada con el ranking final
            
        Raises:
            HTTPException: Si el campeonato no existe o no ha finalizado
        """
        # Verificar que el campeonato ha finalizado
        campeonato = self.db.query(Campeonato).filter(
            Campeonato.id == campeonato_id
        ).first()
        
        if not campeonato:
            raise HTTPException(
                status_code=404,
                detail="Campeonato no encontrado"
            )
            
        if campeonato.partida_actual < campeonato.numero_partidas:
            raise HTTPException(
                status_code=400,
                detail="El campeonato aún no ha finalizado"
            )

        return self.get_ranking(campeonato_id)

    def actualizar_ranking(self, campeonato_id: int) -> Dict[str, str]:
        """
        Actualiza el ranking del campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Mensaje de confirmación
            
        Raises:
            HTTPException: Si hay error en la actualización
        """
        try:
            # Aquí podrías agregar lógica adicional para actualizar el ranking
            # Por ejemplo, recalcular posiciones o actualizar estadísticas
            
            return {"message": "Ranking actualizado correctamente"}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al actualizar el ranking: {str(e)}"
            )

    def get_ranking_por_grupo(
        self,
        campeonato_id: int,
        grupo: str
    ) -> List[Dict[str, Any]]:
        """
        Obtiene el ranking filtrado por grupo específico.
        
        Args:
            campeonato_id: ID del campeonato
            grupo: Grupo a filtrar ('A' o 'B')
            
        Returns:
            Lista filtrada del ranking para el grupo especificado
            
        Raises:
            HTTPException: Si el grupo es inválido
        """
        if grupo not in ['A', 'B']:
            raise HTTPException(
                status_code=400,
                detail="Grupo inválido. Debe ser 'A' o 'B'"
            )

        ranking_completo = self.get_ranking(campeonato_id)
        return [r for r in ranking_completo if r['GB'] == grupo]

    def get_ranking_pareja(
        self,
        campeonato_id: int,
        pareja_id: int
    ) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de resultados de una pareja específica.
        
        Args:
            campeonato_id: ID del campeonato
            pareja_id: ID de la pareja
            
        Returns:
            Lista de resultados ordenados por partida
            
        Raises:
            HTTPException: Si no se encuentran resultados
            
        Note:
            Incluye información de mesa, partida, PG, PP, GB y RP
        """
        # Obtener todos los resultados de la pareja ordenados por partida
        resultados = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja_id
        ).order_by(Resultado.P).all()

        if not resultados:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron resultados para esta pareja"
            )

        return [
            {
                'partida': r.P,
                'mesa': r.M,
                'PG': r.PG,
                'PP': r.PP,
                'GB': r.GB,
                'RP': r.RP
            }
            for r in resultados
        ]
