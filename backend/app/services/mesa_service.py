from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.models.resultado import Resultado
from app.schemas.mesa import MesaCreate, MesaConParejas
from typing import List, Optional
import random

class MesaService:
    """
    Servicio que maneja todas las operaciones relacionadas con las mesas de juego.
    Proporciona funcionalidad para crear, gestionar y consultar mesas y sus asignaciones.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de mesas.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_mesa(self, mesa_id: int) -> Optional[Mesa]:
        """
        Obtiene una mesa específica por su ID.
        
        Args:
            mesa_id: ID de la mesa a buscar
            
        Returns:
            Mesa si existe, None en caso contrario
        """
        return self.db.query(Mesa).filter(Mesa.id == mesa_id).first()

    def get_mesas_campeonato(self, campeonato_id: int) -> List[Mesa]:
        """
        Obtiene todas las mesas de un campeonato específico.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de todas las mesas del campeonato
        """
        return self.db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id
        ).all()

    def crear_mesas(self, campeonato_id: int, partida: int) -> List[Mesa]:
        """
        Crea las mesas necesarias para una partida del campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            partida: Número de la partida
            
        Returns:
            Lista de mesas creadas
            
        Raises:
            HTTPException: Si no hay suficientes parejas activas o hay error en la creación
            
        Note:
            - Mezcla aleatoriamente las parejas para asignación
            - Maneja el caso de número impar de parejas
        """
        # Obtener parejas activas del campeonato
        parejas = self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        if len(parejas) < 2:
            raise HTTPException(
                status_code=400,
                detail="No hay suficientes parejas activas para crear mesas"
            )

        # Mezclar parejas aleatoriamente para asignación
        random.shuffle(parejas)
        mesas_creadas = []
        
        # Crear mesas y asignar parejas
        for i in range(0, len(parejas), 2):
            mesa = Mesa(
                campeonato_id=campeonato_id,
                partida=partida,
                numero=i//2 + 1,
                pareja1_id=parejas[i].id,
                pareja2_id=parejas[i+1].id if i+1 < len(parejas) else None
            )
            self.db.add(mesa)
            mesas_creadas.append(mesa)

        try:
            self.db.commit()
            for mesa in mesas_creadas:
                self.db.refresh(mesa)
            return mesas_creadas
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_mesas_con_resultados(
        self,
        campeonato_id: int,
        partida: int
    ) -> List[MesaConParejas]:
        """
        Obtiene las mesas de una partida con información de parejas y resultados.
        
        Args:
            campeonato_id: ID del campeonato
            partida: Número de la partida
            
        Returns:
            Lista de mesas con información detallada de parejas y resultados
        """
        mesas = self.db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id,
            Mesa.partida == partida
        ).all()

        mesas_con_info = []
        for mesa in mesas:
            # Verificar si la mesa tiene resultados registrados
            tiene_resultados = self.verificar_resultados(
                mesa.id,
                partida,
                campeonato_id
            )

            # Obtener información de las parejas asignadas
            pareja1 = self.db.query(Pareja).filter(
                Pareja.id == mesa.pareja1_id
            ).first()
            pareja2 = self.db.query(Pareja).filter(
                Pareja.id == mesa.pareja2_id
            ).first() if mesa.pareja2_id else None

            mesas_con_info.append({
                **mesa.__dict__,
                "tiene_resultados": tiene_resultados,
                "pareja1_nombre": pareja1.nombre if pareja1 else None,
                "pareja2_nombre": pareja2.nombre if pareja2 else None
            })

        return mesas_con_info

    def asignar_parejas(
        self,
        mesa_id: int,
        pareja1_id: int,
        pareja2_id: Optional[int] = None
    ) -> Mesa:
        """
        Asigna o reasigna parejas a una mesa específica.
        
        Args:
            mesa_id: ID de la mesa
            pareja1_id: ID de la primera pareja
            pareja2_id: ID de la segunda pareja (opcional)
            
        Returns:
            Mesa actualizada
            
        Raises:
            HTTPException: Si la mesa no existe o hay error en la asignación
        """
        mesa = self.get_mesa(mesa_id)
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        mesa.pareja1_id = pareja1_id
        mesa.pareja2_id = pareja2_id

        try:
            self.db.commit()
            self.db.refresh(mesa)
            return mesa
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def verificar_resultados(
        self,
        mesa_id: int,
        partida: int,
        campeonato_id: int
    ) -> bool:
        """
        Verifica si una mesa tiene resultados registrados.
        
        Args:
            mesa_id: ID de la mesa
            partida: Número de la partida
            campeonato_id: ID del campeonato
            
        Returns:
            bool: True si la mesa tiene resultados, False en caso contrario
        """
        resultados = self.db.query(Resultado).filter(
            Resultado.M == mesa_id,
            Resultado.P == partida,
            Resultado.campeonato_id == campeonato_id
        ).all()
        return len(resultados) > 0

    def sortear_mesas(self, campeonato_id: int) -> List[dict]:
        """
        Realiza un sorteo aleatorio de mesas para un campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de diccionarios con la información de las mesas sorteadas
            
        Raises:
            HTTPException: Si no hay suficientes parejas o hay error en el sorteo
        """
        # Obtener parejas activas del campeonato
        parejas = self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        if len(parejas) < 4:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 4 parejas activas para realizar el sorteo"
            )

        # Mezclar parejas aleatoriamente
        random.shuffle(parejas)

        # Crear mesas y asignar parejas
        mesas_creadas = []
        for i in range(0, len(parejas), 2):
            mesa = Mesa(
                campeonato_id=campeonato_id,
                numero=i//2 + 1,
                pareja1_id=parejas[i].id,
                pareja2_id=parejas[i+1].id if i+1 < len(parejas) else None
            )
            self.db.add(mesa)
            mesas_creadas.append({
                "numero": mesa.numero,
                "pareja1_id": mesa.pareja1_id,
                "pareja2_id": mesa.pareja2_id
            })

        try:
            self.db.commit()
            return mesas_creadas
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def eliminar_mesas(self, campeonato_id: int):
        """
        Elimina todas las mesas de un campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Raises:
            HTTPException: Si hay error en la eliminación
        """
        try:
            self.db.query(Mesa).filter(
                Mesa.campeonato_id == campeonato_id
            ).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
