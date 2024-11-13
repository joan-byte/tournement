from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, nullable=False)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    partida = Column(Integer, nullable=False)
    pareja1_id = Column(Integer, ForeignKey("parejas.id"))
    pareja2_id = Column(Integer, ForeignKey("parejas.id"), nullable=True)

    # Relaciones
    campeonato = relationship("Campeonato", back_populates="mesas")
    pareja1 = relationship("Pareja", foreign_keys=[pareja1_id], back_populates="mesas_como_pareja1")
    pareja2 = relationship("Pareja", foreign_keys=[pareja2_id], back_populates="mesas_como_pareja2")
    resultados = relationship("Resultado", back_populates="mesa")

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "campeonato_id": self.campeonato_id,
            "partida": self.partida,
            "pareja1_id": self.pareja1_id,
            "pareja2_id": self.pareja2_id,
            "pareja1_nombre": self.pareja1.nombre if self.pareja1 else None,
            "pareja2_nombre": self.pareja2.nombre if self.pareja2 else None
        }
