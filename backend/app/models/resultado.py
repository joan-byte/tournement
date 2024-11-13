from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    P = Column(Integer)  # Partida
    M = Column(Integer, ForeignKey("mesas.id"))  # Mesa
    id_pareja = Column(Integer, ForeignKey("parejas.id"))
    GB = Column(String)  # Grupo
    PG = Column(Integer)  # Puntos Ganados
    PP = Column(Integer)  # Puntos Perdidos
    RP = Column(Integer)  # Resultado Parcial

    # Relaciones
    campeonato = relationship("Campeonato", back_populates="resultados")
    mesa = relationship("Mesa", back_populates="resultados")
    pareja = relationship("Pareja", back_populates="resultados")

    def to_dict(self):
        return {
            "id": self.id,
            "campeonato_id": self.campeonato_id,
            "P": self.P,
            "M": self.M,
            "id_pareja": self.id_pareja,
            "RP": self.RP,
            "PG": self.PG,
            "PP": self.PP,
            "GB": self.GB
        }
