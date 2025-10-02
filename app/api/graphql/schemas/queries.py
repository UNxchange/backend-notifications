# app/api/graphql/schemas/queries.py
import strawberry
from typing import List, Optional
from strawberry.fastapi import BaseContext
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.graphql.schemas.types import (
    User, UserRole, NotificationStats, RecentNotification, 
    ValidationResult, BulkEmailFilters, Notification as NotificationType
)
from app.api.graphql.resolvers.user_resolver import UserResolver
from app.api.graphql.resolvers.notification_resolver import NotificationResolver
from app.db.model import Notification

class Context(BaseContext):
    def __init__(self):
        self.db = next(get_db())

@strawberry.type
class Query:
    # User queries
    @strawberry.field
    def users(
        self, 
        info: strawberry.Info[Context],
        role: Optional[UserRole] = None,
        limit: Optional[int] = None
    ) -> List[User]:
        """Obtener todos los usuarios con filtros opcionales"""
        return UserResolver.get_all_users(info.context.db, role, limit)
    
    @strawberry.field  
    def user(self, info: strawberry.Info[Context], id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return UserResolver.get_user_by_id(info.context.db, id)
    
    @strawberry.field
    def users_by_role(self, info: strawberry.Info[Context], role: UserRole) -> List[User]:
        """Obtener usuarios por rol específico"""
        return UserResolver.get_users_by_role(info.context.db, role)
    
    @strawberry.field
    def users_by_email_domain(self, info: strawberry.Info[Context], domain: str) -> List[User]:
        """Obtener usuarios por dominio de email"""
        return UserResolver.get_users_by_email_domain(info.context.db, domain)
    
    # Notification queries
    @strawberry.field
    def notifications(self, info: strawberry.Info[Context], user_id: int) -> List[NotificationType]:
        """Obtener todas las notificaciones de un usuario"""
        db_notifications = info.context.db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(Notification.created_at.desc()).all()
        
        return [NotificationType(
            id=n.id,
            user_id=n.user_id,
            type=n.type,
            title=n.title,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at.isoformat() if n.created_at else "",
            read_at=n.read_at.isoformat() if n.read_at else None,
            metadata=n.extra_data or {}
        ) for n in db_notifications]
    
    @strawberry.field
    def unread_notifications(self, info: strawberry.Info[Context], user_id: int) -> List[NotificationType]:
        """Obtener notificaciones no leídas de un usuario"""
        db_notifications = info.context.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).order_by(Notification.created_at.desc()).all()
        
        return [NotificationType(
            id=n.id,
            user_id=n.user_id,
            type=n.type,
            title=n.title,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at.isoformat() if n.created_at else "",
            read_at=n.read_at.isoformat() if n.read_at else None,
            metadata=n.extra_data or {}
        ) for n in db_notifications]
    
    @strawberry.field
    def notification(self, info: strawberry.Info[Context], notification_id: int) -> Optional[NotificationType]:
        """Obtener una notificación específica"""
        n = info.context.db.query(Notification).filter(Notification.id == notification_id).first()
        if not n:
            return None
        
        return NotificationType(
            id=n.id,
            user_id=n.user_id,
            type=n.type,
            title=n.title,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at.isoformat() if n.created_at else "",
            read_at=n.read_at.isoformat() if n.read_at else None,
            metadata=n.extra_data or {}
        )
    
    # Stats queries
    @strawberry.field
    def notification_stats(self, info: strawberry.Info[Context]) -> NotificationStats:
        """Obtener estadísticas de notificaciones"""
        return NotificationResolver.get_notification_stats(info.context.db)
    
    @strawberry.field
    def recent_notifications(
        self, 
        info: strawberry.Info[Context], 
        limit: int = 10
    ) -> List[RecentNotification]:
        """Obtener notificaciones recientes"""
        return NotificationResolver.get_recent_notifications(info.context.db, limit)
    
    @strawberry.field
    def validate_bulk_email(
        self, 
        info: strawberry.Info[Context],
        filters: Optional[BulkEmailFilters] = None
    ) -> ValidationResult:
        """Validar envío masivo antes de ejecutar"""
        return NotificationResolver.validate_bulk_email(info.context.db, filters)