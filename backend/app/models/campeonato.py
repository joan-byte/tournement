from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.core.constants import EstadoCampeonato

class Campeonato(Base):
    """
    Modelo que representa un campeonato en la base de datos.
    Hereda de Base para obtener funcionalidad común de SQLAlchemy.
    
    Attributes:
        id (int): Identificador único del campeonato
        nombre (str): Nombre del campeonato
        fecha_inicio (Date): Fecha de inicio del campeonato
        dias_duracion (int): Duración en días del campeonato
        numero_partidas (int): Número total de partidas programadas
        grupo_b (bool): Indica si existe grupo B en el campeonato
        partida_actual (int): Número de la partida actual en curso
    """
    __tablename__ = "campeonatos"
    __table_args__ = {'extend_existing': True}

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    fecha_inicio = Column(Date)
    dias_duracion = Column(Integer)
    numero_partidas = Column(Integer)
    grupo_b = Column(Boolean, default=False)
    partida_actual = Column(Integer, default=0)

    # Relaciones con otras tablas
    # Cada relación define una conexión bidireccional con otros modelos
    parejas = relationship("Pareja", back_populates="campeonato")      # Relación uno a muchos con Pareja
    jugadores = relationship("Jugador", back_populates="campeonato")   # Relación uno a muchos con Jugador
    mesas = relationship("Mesa", back_populates="campeonato")          # Relación uno a muchos con Mesa
    resultados = relationship("Resultado", back_populates="campeonato") # Relación uno a muchos con Resultado

    def __repr__(self):
        """
        Representación en string del objeto Campeonato.
        Returns:
            str: Representación legible del campeonato
        """
        return f"<Campeonato {self.nombre}>"

    def to_dict(self):
        """
        Convierte el objeto Campeonato a un diccionario.
        Útil para serialización y respuestas API.
        
        Returns:
            dict: Diccionario con los atributos del campeonato
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "dias_duracion": self.dias_duracion,
            "numero_partidas": self.numero_partidas,
            "grupo_b": self.grupo_b,
            "partida_actual": self.partida_actual
        }

    @property
    def estado(self) -> EstadoCampeonato:
        """
        Determina el estado actual del campeonato basado en la partida actual.
        
        Returns:
            EstadoCampeonato: Estado actual del campeonato (INSCRIPCION, ACTIVO, FINALIZADO)
        """
        if self.partida_actual == 0:
            return EstadoCampeonato.INSCRIPCION
        elif self.partida_actual < self.numero_partidas:
            return EstadoCampeonato.ACTIVO
        else:
            return EstadoCampeonato.FINALIZADO

    @property
    def parejas_activas(self):
        """
        Obtiene la lista de parejas activas en el campeonato.
        
        Returns:
            list: Lista de parejas que están activas en el campeonato
        """
        return [p for p in self.parejas if p.activa]

    @property
    def total_parejas(self):
        """
        Calcula el número total de parejas en el campeonato.
        
        Returns:
            int: Número total de parejas registradas
        """
        return len(self.parejas)

    @property
    def total_parejas_activas(self):
        """
        Calcula el número total de parejas activas en el campeonato.
        
        Returns:
            int: Número de parejas activas
        """
        return len(self.parejas_activas)

    def puede_iniciar_partida(self) -> bool:
        """
        Verifica si el campeonato puede iniciar una nueva partida.
        
        Returns:
            bool: True si se puede iniciar una partida, False en caso contrario
        """
        from app.core.constants import MINIMO_PAREJAS_TORNEO
        return (
            self.estado == EstadoCampeonato.INSCRIPCION and
            self.total_parejas_activas >= MINIMO_PAREJAS_TORNEO
        )

    def puede_finalizar_partida(self) -> bool:
        """
        Verifica si se puede finalizar la partida actual.
        
        Returns:
            bool: True si se puede finalizar la partida actual, False en caso contrario
        """
        return (
            self.estado == EstadoCampeonato.ACTIVO and
            self.partida_actual > 0 and
            self.partida_actual <= self.numero_partidas
        )
