from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.pareja import Pareja
from app.models.jugador import Jugador
from app.schemas.pareja import ParejaCreate, ParejaUpdate
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

class ParejaService:
    """
    Servicio que maneja todas las operaciones relacionadas con parejas de jugadores.
    Proporciona funcionalidad para crear, actualizar, eliminar y consultar parejas,
    así como gestionar sus jugadores asociados.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de parejas.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_parejas(
        self,
        skip: int = 0,
        limit: int = 100,
        campeonato_id: int = None
    ) -> List[dict]:
        """
        Obtiene una lista paginada de parejas, opcionalmente filtrada por campeonato.
        
        Args:
            skip: Número de registros a saltar (para paginación)
            limit: Número máximo de registros a devolver
            campeonato_id: ID del campeonato para filtrar (opcional)
            
        Returns:
            Lista de diccionarios con información de las parejas
        """
        # Construir la consulta base
        query = self.db.query(Pareja)
        
        # Aplicar filtro por campeonato si se especifica
        if campeonato_id:
            query = query.filter(Pareja.campeonato_id == campeonato_id)
        
        # Ordenar por número descendente y aplicar paginación
        query = query.order_by(Pareja.numero.desc())
        parejas = query.offset(skip).limit(limit).all()
        
        # Convertir resultados a diccionarios con la información necesaria
        return [
            {
                "id": p.id,
                "numero": p.numero,
                "nombre": p.nombre,
                "club": p.club,
                "activa": p.activa,
                "campeonato_id": p.campeonato_id
            }
            for p in parejas
        ]

    def get_pareja(self, pareja_id: int) -> Optional[Pareja]:
        """
        Obtiene una pareja específica por su ID.
        
        Args:
            pareja_id: ID de la pareja a buscar
            
        Returns:
            Objeto Pareja si existe, None en caso contrario
        """
        return self.db.query(Pareja).filter(Pareja.id == pareja_id).first()

    def create_pareja(self, pareja: ParejaCreate) -> Pareja:
        """
        Crea una nueva pareja con sus jugadores asociados.
        
        Args:
            pareja: Datos de la pareja y sus jugadores a crear
            
        Returns:
            Pareja creada
            
        Raises:
            HTTPException: Si hay errores de integridad o en la creación
            
        Note:
            - Asigna automáticamente el siguiente número disponible en el campeonato
            - Crea los dos jugadores asociados a la pareja
        """
        # Obtener el último número de pareja para este campeonato
        ultimo_numero = self.db.query(Pareja).filter(
            Pareja.campeonato_id == pareja.campeonato_id
        ).order_by(Pareja.numero.desc()).first()

        # Asignar el siguiente número
        nuevo_numero = 1 if not ultimo_numero else ultimo_numero.numero + 1

        # Crear la pareja con el nuevo número
        db_pareja = Pareja(
            nombre=pareja.nombre,
            club=pareja.club,
            campeonato_id=pareja.campeonato_id,
            numero=nuevo_numero
        )
        self.db.add(db_pareja)
        
        try:
            self.db.flush()  # Para obtener el ID de la pareja
            
            # Crear los jugadores asociados
            jugador1 = Jugador(
                nombre=pareja.jugador1.nombre,
                apellido=pareja.jugador1.apellido,
                pareja_id=db_pareja.id,
                campeonato_id=pareja.campeonato_id
            )
            jugador2 = Jugador(
                nombre=pareja.jugador2.nombre,
                apellido=pareja.jugador2.apellido,
                pareja_id=db_pareja.id,
                campeonato_id=pareja.campeonato_id
            )
            
            self.db.add(jugador1)
            self.db.add(jugador2)
            self.db.commit()
            self.db.refresh(db_pareja)
            return db_pareja
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error de integridad en la base de datos"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_pareja(self, pareja_id: int, pareja: ParejaUpdate) -> Optional[Pareja]:
        """
        Actualiza los datos de una pareja existente.
        
        Args:
            pareja_id: ID de la pareja a actualizar
            pareja: Nuevos datos de la pareja
            
        Returns:
            Pareja actualizada o None si no existe
            
        Raises:
            HTTPException: Si hay errores en la actualización
        """
        db_pareja = self.get_pareja(pareja_id)
        if not db_pareja:
            return None

        # Actualizar solo los campos proporcionados
        for key, value in pareja.model_dump(exclude_unset=True).items():
            if key not in ['jugador1', 'jugador2']:
                setattr(db_pareja, key, value)

        try:
            self.db.commit()
            self.db.refresh(db_pareja)
            return db_pareja
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def delete_pareja(self, pareja_id: int) -> bool:
        """
        Elimina una pareja y sus jugadores asociados.
        
        Args:
            pareja_id: ID de la pareja a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            HTTPException: Si hay errores durante la eliminación
        """
        try:
            # Primero eliminamos los jugadores asociados
            self.db.query(Jugador).filter(Jugador.pareja_id == pareja_id).delete()
            
            # Luego eliminamos la pareja
            result = self.db.query(Pareja).filter(Pareja.id == pareja_id).delete()
            
            self.db.commit()
            return result > 0
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"No se puede eliminar la pareja: {str(e)}"
            )

    def activar_pareja(self, pareja_id: int) -> Optional[Pareja]:
        """
        Activa una pareja para participar en el campeonato.
        
        Args:
            pareja_id: ID de la pareja a activar
            
        Returns:
            Pareja activada o None si no existe
        """
        db_pareja = self.get_pareja(pareja_id)
        if not db_pareja:
            return None

        db_pareja.activa = True
        self.db.commit()
        self.db.refresh(db_pareja)
        return db_pareja

    def desactivar_pareja(self, pareja_id: int) -> Optional[Pareja]:
        """
        Desactiva una pareja del campeonato.
        
        Args:
            pareja_id: ID de la pareja a desactivar
            
        Returns:
            Pareja desactivada o None si no existe
        """
        db_pareja = self.get_pareja(pareja_id)
        if not db_pareja:
            return None

        db_pareja.activa = False
        self.db.commit()
        self.db.refresh(db_pareja)
        return db_pareja

    def get_parejas_activas(self, campeonato_id: int) -> List[Pareja]:
        """
        Obtiene todas las parejas activas de un campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de parejas activas en el campeonato
        """
        return self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

    def get_parejas_campeonato(self, campeonato_id: int):
        """
        Obtiene todas las parejas de un campeonato ordenadas por número.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de parejas del campeonato o lista vacía si no hay parejas
        """
        # Obtener las parejas ordenadas por número descendente
        parejas = self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id
        ).order_by(Pareja.numero.desc()).all()
        
        if not parejas:
            return []
        
        return parejas

    def get_pareja_con_jugadores(self, pareja_id: int):
        """
        Obtiene una pareja con información detallada de sus jugadores.
        
        Args:
            pareja_id: ID de la pareja
            
        Returns:
            Diccionario con información de la pareja y sus jugadores
            
        Raises:
            HTTPException: Si la pareja no existe
        """
        pareja = self.db.query(Pareja).filter(Pareja.id == pareja_id).first()
        if not pareja:
            raise HTTPException(status_code=404, detail="Pareja no encontrada")
        
        # Obtener los jugadores asociados
        jugadores = self.db.query(Jugador).filter(
            Jugador.pareja_id == pareja_id
        ).order_by(Jugador.id).all()
        
        # Construir respuesta con información completa
        return {
            "id": pareja.id,
            "numero": pareja.numero,
            "nombre": pareja.nombre,
            "club": pareja.club,
            "activa": pareja.activa,
            "campeonato_id": pareja.campeonato_id,
            "jugadores": [
                {
                    "id": j.id,
                    "nombre": j.nombre,
                    "apellido": j.apellido,
                    "campeonato_id": j.campeonato_id
                }
                for j in jugadores
            ]
        }
  