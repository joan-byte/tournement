# Importaciones necesarias para la configuración de la base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
# Esto permite mantener las configuraciones sensibles fuera del código
load_dotenv()

# Obtiene las credenciales y configuración de la base de datos desde variables de entorno
# Estas variables deben estar definidas en el archivo .env
DB_USER = os.getenv("POSTGRES_USER")        # Usuario de PostgreSQL
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") # Contraseña de PostgreSQL
DB_HOST = os.getenv("POSTGRES_SERVER")      # Host del servidor PostgreSQL
DB_NAME = os.getenv("POSTGRES_DB")          # Nombre de la base de datos

# Construye la URL de conexión para PostgreSQL usando el formato estándar
# Format: postgresql://username:password@host/database_name
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Crea el engine de SQLAlchemy que manejará la conexión con la base de datos
# Este es el punto central de conexión con la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea una fábrica de sesiones configurada con las opciones especificadas
# autocommit=False: Las transacciones deben ser confirmadas explícitamente
# autoflush=False: Los cambios no se envían automáticamente a la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Generador de contexto que proporciona una sesión de base de datos.
    
    Yields:
        Session: Una sesión de base de datos activa
    
    Note:
        - La sesión se cierra automáticamente después de su uso
        - Utilizar con 'with' o en un contexto de dependencia FastAPI
        - Maneja automáticamente el cierre de la sesión incluso si hay excepciones
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Clase base para los modelos SQLAlchemy
# Todos los modelos de la aplicación deben heredar de esta clase
Base = declarative_base()
