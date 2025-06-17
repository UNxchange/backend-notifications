# app/api/endpoints.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import obtener_emails, get_all_users
from app.core.email import enviar_email
from app.api.v1.schemas import UserOut
from app.crud import user as crud_user

router = APIRouter()

@router.post("/enviar-correo/")
def enviar_correos(db: Session = Depends(get_db)):
    emails = obtener_emails(db)
    for email in emails:
        enviar_email(email, "Asunto", "Este es el contenido del correo")
    return {"message": f"Correos enviados a {len(emails)} usuarios"}

@router.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)
