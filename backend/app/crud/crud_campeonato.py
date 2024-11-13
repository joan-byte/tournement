from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.campeonato import Campeonato
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate

class CRUDCampeonato(CRUDBase[Campeonato, CampeonatoCreate, CampeonatoUpdate]):
    pass

campeonato = CRUDCampeonato(Campeonato) 