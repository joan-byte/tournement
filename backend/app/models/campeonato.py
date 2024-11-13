from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.core.constants import EstadoCampeonato

class Campeonato(Base):
    __tablename__ = "campeonatos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    fecha_inicio = Column(Date)
    dias_duracion = Column(Integer)
    numero_partidas = Column(Integer)
    grupo_b = Column(Boolean, default=False)
    partida_actual = Column(Integer, default=0)

    # Relaciones
    parejas = relationship("Pareja", back_populates="campeonato")
    jugadores = relationship("Jugador", back_populates="campeonato")
    mesas = relationship("Mesa", back_populates="campeonato")
    resultados = relationship("Resultado", back_populates="campeonato")

    def __repr__(self):
        return f"<Campeonato {self.nombre}>"

    def to_dict(self):
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
        if self.partida_actual == 0:
            return EstadoCampeonato.INSCRIPCION
        elif self.partida_actual < self.numero_partidas:
            return EstadoCampeonato.ACTIVO
        else:
            return EstadoCampeonato.FINALIZADO

    @property
    def parejas_activas(self):
        return [p for p in self.parejas if p.activa]

    @property
    def total_parejas(self):
        return len(self.parejas)

    @property
    def total_parejas_activas(self):
        return len(self.parejas_activas)

    def puede_iniciar_partida(self) -> bool:
        from app.core.constants import MINIMO_PAREJAS_TORNEO
        return (
            self.estado == EstadoCampeonato.INSCRIPCION and
            self.total_parejas_activas >= MINIMO_PAREJAS_TORNEO
        )

    def puede_finalizar_partida(self) -> bool:
        return (
            self.estado == EstadoCampeonato.ACTIVO and
            self.partida_actual > 0 and
            self.partida_actual <= self.numero_partidas
        )
