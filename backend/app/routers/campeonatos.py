# Importaciones necesarias para definir las rutas y manejar las solicitudes
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.campeonato import Campeonato
from app.models.pareja import Pareja
from app.models.jugador import Jugador
from app.models.mesa import Mesa
from app.models.resultado import Resultado
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate
from datetime import date
from sqlalchemy import text, func
from contextlib import contextmanager
from sqlalchemy.exc import OperationalError

# Creación de un enrutador para manejar las rutas relacionadas con campeonatos
router = APIRouter()

@contextmanager
def transaction_lock(db: Session):
    """
    Ejecuta operaciones en una transacción bloqueada.
    Utiliza un bloqueo exclusivo en la tabla campeonatos para evitar operaciones concurrentes.
    
    Args:
        db: Sesión de la base de datos
    
    Yields:
        Control de la transacción bloqueada
    """
    try:
        # Bloquear la tabla para evitar operaciones concurrentes
        db.execute(text("LOCK TABLE campeonatos IN EXCLUSIVE MODE"))
        yield
    finally:
        db.commit()

@router.get("/")
def get_campeonatos(db: Session = Depends(get_db)):
    """
    Obtiene todos los campeonatos de la base de datos.
    
    Args:
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        Lista de todos los campeonatos
    """
    return db.query(Campeonato).all()

@router.get("/{campeonato_id}")
def get_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un campeonato específico por su ID.
    
    Args:
        campeonato_id: ID del campeonato a obtener
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        El campeonato solicitado o un error 404 si no se encuentra
    """
    try:
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        # Forzar la carga de los datos antes de devolver
        db.refresh(campeonato)
        
        # Log para depuración
        print(f"Devolviendo campeonato: {campeonato.id} - {campeonato.nombre}")
        
        return campeonato
    except Exception as e:
        print(f"Error al obtener campeonato: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_campeonato(campeonato: CampeonatoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo campeonato en la base de datos.
    
    Args:
        campeonato: Datos del campeonato a crear
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        El campeonato creado
    """
    try:
        db_campeonato = Campeonato(
            nombre=campeonato.nombre,
            fecha_inicio=campeonato.fecha_inicio,
            dias_duracion=campeonato.dias_duracion,
            numero_partidas=campeonato.numero_partidas,
            grupo_b=campeonato.grupo_b,
            partida_actual=0
        )
        db.add(db_campeonato)
        db.commit()
        db.refresh(db_campeonato)
        return db_campeonato
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{campeonato_id}")
def update_campeonato(
    campeonato_id: int, 
    campeonato_data: CampeonatoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un campeonato existente.
    
    Args:
        campeonato_id: ID del campeonato a actualizar
        campeonato_data: Datos actualizados del campeonato
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        El campeonato actualizado o un error 404 si no se encuentra
    """
    try:
        campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        for key, value in campeonato_data.dict(exclude_unset=True).items():
            setattr(campeonato, key, value)
        
        db.commit()
        db.refresh(campeonato)
        
        # Log para depuración
        print(f"Campeonato actualizado: {campeonato.id} - {campeonato.nombre}")
        
        return campeonato
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar campeonato: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{campeonato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Elimina un campeonato y sus datos relacionados de la base de datos.
    
    Args:
        campeonato_id: ID del campeonato a eliminar
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        Mensaje de éxito o un error 404 si no se encuentra
    """
    try:
        with transaction_lock(db):
            # Verificar que el campeonato existe
            campeonato = db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
            if not campeonato:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Campeonato no encontrado"
                )

            # Eliminar datos relacionados en orden
            db.query(Resultado).filter(Resultado.campeonato_id == campeonato_id).delete(synchronize_session=False)
            db.query(Mesa).filter(Mesa.campeonato_id == campeonato_id).delete(synchronize_session=False)
            db.query(Jugador).filter(Jugador.campeonato_id == campeonato_id).delete(synchronize_session=False)
            db.query(Pareja).filter(Pareja.campeonato_id == campeonato_id).delete(synchronize_session=False)
            db.query(Campeonato).filter(Campeonato.id == campeonato_id).delete(synchronize_session=False)

            # Verificar si quedan campeonatos de forma segura
            remaining_count = db.query(func.count(Campeonato.id)).scalar()
            
            if remaining_count == 0:
                try:
                    db.execute(text("ALTER SEQUENCE campeonatos_id_seq RESTART WITH 1"))
                except OperationalError as e:
                    print(f"No se pudo reiniciar la secuencia de IDs: {str(e)}")
                    # No lanzamos el error para que la operación principal se complete
        
        return {"message": "Campeonato eliminado correctamente"}
        
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar campeonato: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el campeonato: {str(e)}"
        ) 