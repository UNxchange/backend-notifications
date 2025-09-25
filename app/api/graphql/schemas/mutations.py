# app/api/graphql/schemas/mutations.py
import strawberry
from typing import Optional
from strawberry.fastapi import BaseContext
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.graphql.schemas.types import (
    NotificationResult, WelcomeEmailInput, ConvocatoriaInput, 
    BulkEmailInput, UserInput, UserWithNotification, User, UserRole
)
from app.api.graphql.resolvers.notification_resolver import NotificationResolver
from app.api.graphql.resolvers.user_resolver import UserResolver
from app.crud import user as crud_user
from app.core.email import enviar_correo_confirmacion
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
            # Simular creación de usuario (en producción usarías el microservicio de auth)
            # Por ahora solo enviamos el correo de bienvenida y simulamos la respuesta
            
            # Enviar correo de bienvenida
            welcome_result = NotificationResolver.send_welcome_email(
                info.context.db,
                input.name,
                input.email
            )
            
            # Simular usuario creado
            user = User(
                id=999,  # ID simulado
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
                id=0,
                name=input.name,
                email=input.email,
                role=input.role
            )
            
            return UserWithNotification(
                user=user,
                welcome_email=error_result,
                total_users=0
            )