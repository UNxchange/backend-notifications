# app/db/models.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, JSON
from datetime import datetime
from .session import Base
import enum

class UserRole(str, enum.Enum):
    estudiante = "estudiante"
    profesional = "profesional"
    administrador = "administrador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False) # name prueba
    role = Column(String, nullable=False, default=UserRole.estudiante.value)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # role = Column(Enum(UserRole), nullable=False, default=UserRole.estudiante)
    # Podríamos añadir más campos como: full_name, is_active, etc.

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    type = Column(String, nullable=False)  # convocatoria, application, approval, rejection, reminder, message
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Additional data as JSON (changed from metadata)