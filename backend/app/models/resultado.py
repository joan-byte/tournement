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
    PT = Column(Integer)

    # Relaciones
    campeonato = relationship("Campeonato", back_populates="resultados")
    mesa = relationship("Mesa", back_populates="resultados")
    pareja = relationship("Pareja", back_populates="resultados")

    def calcular_puntos_totales(self):
        if self.RP > 0:
            self.PT = 2 + self.RP
        elif self.PG >= 50:
            self.PT = 1
        else:
            self.PT = 0

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
            "RP": self.RP,
            "PT": self.PT
        }

@event.listens_for(Resultado, 'before_insert')
@event.listens_for(Resultado, 'before_update')
def calcular_campos(mapper, connection, target):
    target.RP = target.PG - target.PP
    target.calcular_puntos_totales()
