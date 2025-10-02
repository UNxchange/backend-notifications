# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crea el motor de la base de datos con configuración de pool optimizada
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,              # Tamaño base del pool (antes era 5)
    max_overflow=40,           # Conexiones adicionales permitidas (antes era 10)
    pool_timeout=60,           # Timeout para obtener conexión (antes era 30)
    pool_pre_ping=True,        # Verifica conexión antes de usar
    pool_recycle=3600,         # Recicla conexiones cada hora
    echo=False                 # No mostrar SQL queries en logs
)
print("Connection Success")
# Crea una fábrica de sesiones (SessionLocal) que se usará para crear nuevas sesiones de DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es una clase base para nuestros modelos ORM. Heredarán de ella.
Base = declarative_base()

# Función de dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()