# app/api/v1/schemas.py
from pydantic import BaseModel, EmailStr

from app.db.model import UserRole

# Schema para mostrar la info de un usuario (sin la contraseña)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True # Permite que Pydantic lea datos desde modelos ORM

# Schema para notificación de usuario creado
class UserCreatedNotification(BaseModel):
    name: str
    email: EmailStr

# Schema para notificación de convocatoria elegida
class ConvocatoriaElegidaNotification(BaseModel):
    user_name: str
    user_email: EmailStr
    convocatoria_titulo: str
    convocatoria_descripcion: str
    universidad_destino: str
    fecha_inicio: str
    fecha_fin: str
    
# Schema para respuesta de notificación
class NotificationResponse(BaseModel):
    success: bool
    message: str