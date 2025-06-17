# app/crud/usuario.py
from sqlalchemy.orm import Session
from app.db.model import User

def obtener_emails(db: Session):
    return [usuario.email for usuario in db.query(User).all()]

def get_all_users(db: Session):
    """
    Retorna todos los usuarios en la base de datos.
    """
    return db.query(User).all()
