# app/api/graphql/schemas/queries.py
import strawberry
from typing import List, Optional
from strawberry.fastapi import BaseContext
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.graphql.schemas.types import (
    User, UserRole, NotificationStats, RecentNotification, 
    ValidationResult, BulkEmailFilters
)
from app.api.graphql.resolvers.user_resolver import UserResolver
from app.api.graphql.resolvers.notification_resolver import NotificationResolver

class Context(BaseContext):
    def __init__(self):
        self.db = next(get_db())

@strawberry.type
class Query:
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