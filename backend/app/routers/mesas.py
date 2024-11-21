from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Mesa, Pareja

# Creación de un enrutador para manejar las rutas relacionadas con mesas
router = APIRouter()

@router.get("/")
def get_mesas(db: Session = Depends(get_db)):
    """
    Obtiene todas las mesas de la base de datos.
    
    Args:
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        Lista de todas las mesas
    """
    return db.query(Mesa).all()

@router.get("/{mesa_id}")
async def get_mesa(mesa_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una mesa específica por su ID.
    
    Args:
        mesa_id: ID de la mesa a obtener
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        La mesa solicitada con sus parejas relacionadas o un error 404 si no se encuentra
    """
    try:
        # Buscar la mesa por ID
        mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Cargar las parejas relacionadas
        mesa.pareja1 = db.query(Pareja).filter(Pareja.id == mesa.pareja1_id).first()
        if mesa.pareja2_id:
            mesa.pareja2 = db.query(Pareja).filter(Pareja.id == mesa.pareja2_id).first()

        return mesa
    except Exception as e:
        # Manejo de excepciones y retorno de un error 500 en caso de fallo
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener la mesa: {str(e)}"
        ) 