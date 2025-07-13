# app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import obtener_emails, get_all_users
from app.core.email import enviar_email, enviar_correo_confirmacion, enviar_correo_convocatoria_elegida
from app.api.v1.schemas import UserOut, UserCreatedNotification, ConvocatoriaElegidaNotification, NotificationResponse
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

@router.post("/convocatoria-elegida/", response_model=NotificationResponse)
def notificar_convocatoria_elegida(convocatoria_data: ConvocatoriaElegidaNotification):
    """
    Endpoint para recibir notificaciones cuando un usuario elige una convocatoria
    desde el microservicio de convocatorias y enviar correo de confirmación
    """
    try:
        # Enviar correo de confirmación de convocatoria elegida
        enviar_correo_convocatoria_elegida(
            destinatario=convocatoria_data.user_email,
            nombre_usuario=convocatoria_data.user_name,
            titulo_convocatoria=convocatoria_data.convocatoria_titulo,
            descripcion_convocatoria=convocatoria_data.convocatoria_descripcion,
            universidad_destino=convocatoria_data.universidad_destino,
            fecha_inicio=convocatoria_data.fecha_inicio,
            fecha_fin=convocatoria_data.fecha_fin
        )
        
        return NotificationResponse(
            success=True,
            message=f"Correo de confirmación de convocatoria enviado exitosamente a {convocatoria_data.user_email}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar correo de confirmación de convocatoria: {str(e)}"
        )
