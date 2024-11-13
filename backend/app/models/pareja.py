from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Pareja(Base):
    __tablename__ = "parejas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    club = Column(String, nullable=True)
    activa = Column(Boolean, default=True)
    numero = Column(Integer)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))

    jugadores = relationship("Jugador", back_populates="pareja")
    campeonato = relationship("Campeonato", back_populates="parejas")
    mesas_como_pareja1 = relationship("Mesa", foreign_keys="Mesa.pareja1_id", back_populates="pareja1")
    mesas_como_pareja2 = relationship("Mesa", foreign_keys="Mesa.pareja2_id", back_populates="pareja2")
    resultados = relationship("Resultado", back_populates="pareja")

    def __repr__(self):
        return f"<Pareja {self.nombre}>"
