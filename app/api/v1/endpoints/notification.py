# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import obtener_emails, get_all_users
from app.core.email import enviar_email, enviar_correo_confirmacion
from app.api.v1.schemas import UserOut, UserCreatedNotification, NotificationResponse
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

@router.post("/usuario-creado/", response_model=NotificationResponse)
def notificar_usuario_creado(user_data: UserCreatedNotification):
    """
    Endpoint para recibir notificaciones de usuarios creados desde el microservicio de autenticación
    y enviar correo de confirmación
    """
    try:
        # Enviar correo de confirmación
        enviar_correo_confirmacion(user_data.email, user_data.name)
        
        return NotificationResponse(
            success=True,
            message=f"Correo de confirmación enviado exitosamente a {user_data.email}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar correo de confirmación: {str(e)}"
        )
