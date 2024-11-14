from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    partida = Column(Integer)
    id_pareja = Column(Integer, ForeignKey("parejas.id"))
    GB = Column(String)
    PG = Column(Integer)
    PP = Column(Integer)
    RP = Column(Integer)

    # Relaciones
    campeonato = relationship("Campeonato", back_populates="resultados")
    mesa = relationship("Mesa", back_populates="resultados")
    pareja = relationship("Pareja", back_populates="resultados")

    def to_dict(self):
        return {
            "id": self.id,
            "campeonato_id": self.campeonato_id,
            "mesa_id": self.mesa_id,
            "partida": self.partida,
            "id_pareja": self.id_pareja,
            "GB": self.GB,
            "PG": self.PG,
            "PP": self.PP,
            "RP": self.RP
        }

@event.listens_for(Resultado, 'before_insert')
@event.listens_for(Resultado, 'before_update')
def calcular_campos(mapper, connection, target):
    target.PG = 1 if target.PP > 0 else 0
