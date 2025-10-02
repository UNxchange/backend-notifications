# app/api/graphql/schemas/mutations.py
import strawberry
from typing import Optional
from strawberry.fastapi import BaseContext
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.graphql.schemas.types import (
    NotificationResult, WelcomeEmailInput, ConvocatoriaInput, 
    BulkEmailInput, UserInput, UserWithNotification, User, UserRole,
    Notification as NotificationType, NotificationInput
)
from app.api.graphql.resolvers.notification_resolver import NotificationResolver
from app.api.graphql.resolvers.user_resolver import UserResolver
from app.crud import user as crud_user
from app.core.email import enviar_correo_confirmacion
from app.db.model import Notification
from datetime import datetime

class Context(BaseContext):
    def __init__(self):
        self.db = next(get_db())

@strawberry.type
class Mutation:
    @strawberry.mutation
    def send_welcome_email(
        self, 
        info: strawberry.Info[Context],
        input: WelcomeEmailInput
    ) -> NotificationResult:
        """Enviar correo de bienvenida"""
        return NotificationResolver.send_welcome_email(
            info.context.db, 
            input.name, 
            input.email
        )
    
    @strawberry.mutation
    def send_convocatoria_notification(
        self, 
        info: strawberry.Info[Context],
        input: ConvocatoriaInput
    ) -> NotificationResult:
        """Enviar notificación de convocatoria elegida"""
        return NotificationResolver.send_convocatoria_notification(
            info.context.db,
            input.user_name,
            input.user_email,
            input.convocatoria_titulo,
            input.convocatoria_descripcion,
            input.universidad_destino,
            input.fecha_inicio,
            input.fecha_fin
        )
    
    @strawberry.mutation
    def send_bulk_email(
        self, 
        info: strawberry.Info[Context],
        input: BulkEmailInput
    ) -> NotificationResult:
        """Enviar correo masivo con filtros"""
        return NotificationResolver.send_bulk_email(
            info.context.db,
            input.subject,
            input.content,
            input.filters
        )
    
    @strawberry.mutation
    def create_user_with_welcome(
        self, 
        info: strawberry.Info[Context],
        input: UserInput
    ) -> UserWithNotification:
        """Crear usuario y enviar correo de bienvenida automáticamente"""
        try:
            # Usar el ID real del usuario si se proporciona, sino usar 999 como temporal
            user_id = input.id if input.id else 999
            
            # Enviar correo de bienvenida
            welcome_result = NotificationResolver.send_welcome_email(
                info.context.db,
                input.name,
                input.email
            )
            
            # Crear notificación en la base de datos con el ID real del usuario
            try:
                db_notification = Notification(
                    user_id=user_id,  # Usar ID real del usuario
                    type="welcome",
                    title="¡Bienvenido a UNXchange!",
                    message=f"Hola {input.name}, tu cuenta ha sido creada exitosamente.",
                    extra_data={
                        "email": input.email,
                        "role": input.role.value,
                        "action_required": False
                    },
                    is_read=False,
                    created_at=datetime.utcnow()
                )
                info.context.db.add(db_notification)
                info.context.db.commit()
                info.context.db.refresh(db_notification)
                print(f"✅ Notificación de bienvenida creada para usuario ID {user_id}: {input.email}")
            except Exception as e:
                print(f"⚠️ Error creando notificación en DB: {e}")
                # No fallar si no se puede crear la notificación
            
            # Devolver usuario con el ID real
            user = User(
                id=user_id,
                name=input.name,
                email=input.email,
                role=input.role
            )
            
            # Obtener total de usuarios
            all_users = crud_user.get_all_users(info.context.db)
            total_users = len(all_users) + 1  # +1 por el usuario "creado"
            
            return UserWithNotification(
                user=user,
                welcome_email=welcome_result,
                total_users=total_users
            )
        except Exception as e:
            # En caso de error, devolver resultado con error
            error_result = NotificationResult(
                success=False,
                message=f"Error al crear usuario: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
            
            user = User(
                id=input.id if input.id else 0,
                name=input.name,
                email=input.email,
                role=input.role
            )
            
            return UserWithNotification(
                user=user,
                welcome_email=error_result,
                total_users=0
            )
    
    # Notification mutations
    @strawberry.mutation
    def create_notification(
        self,
        info: strawberry.Info[Context],
        notification: NotificationInput
    ) -> NotificationType:
        """Crear una nueva notificación"""
        db_notification = Notification(
            user_id=notification.user_id,
            type=notification.type,
            title=notification.title,
            message=notification.message,
            extra_data=notification.metadata or {},
            is_read=False,
            created_at=datetime.utcnow()
        )
        info.context.db.add(db_notification)
        info.context.db.commit()
        info.context.db.refresh(db_notification)
        
        return NotificationType(
            id=db_notification.id,
            user_id=db_notification.user_id,
            type=db_notification.type,
            title=db_notification.title,
            message=db_notification.message,
            is_read=db_notification.is_read,
            created_at=db_notification.created_at.isoformat(),
            read_at=None,
            metadata=db_notification.extra_data or {}
        )
    
    @strawberry.mutation
    def mark_as_read(
        self,
        info: strawberry.Info[Context],
        notification_id: int
    ) -> NotificationType:
        """Marcar notificación como leída"""
        db_notification = info.context.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not db_notification:
            raise Exception(f"Notification {notification_id} not found")
        
        db_notification.is_read = True
        db_notification.read_at = datetime.utcnow()
        info.context.db.commit()
        info.context.db.refresh(db_notification)
        
        return NotificationType(
            id=db_notification.id,
            user_id=db_notification.user_id,
            type=db_notification.type,
            title=db_notification.title,
            message=db_notification.message,
            is_read=db_notification.is_read,
            created_at=db_notification.created_at.isoformat(),
            read_at=db_notification.read_at.isoformat() if db_notification.read_at else None,
            metadata=db_notification.extra_data or {}
        )
    
    @strawberry.mutation
    def mark_all_as_read(
        self,
        info: strawberry.Info[Context],
        user_id: int
    ) -> bool:
        """Marcar todas las notificaciones como leídas para un usuario"""
        info.context.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({
            "is_read": True,
            "read_at": datetime.utcnow()
        })
        info.context.db.commit()
        return True
    
    @strawberry.mutation
    def delete_notification(
        self,
        info: strawberry.Info[Context],
        notification_id: int
    ) -> bool:
        """Eliminar una notificación"""
        db_notification = info.context.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not db_notification:
            return False
        
        info.context.db.delete(db_notification)
        info.context.db.commit()
        return True