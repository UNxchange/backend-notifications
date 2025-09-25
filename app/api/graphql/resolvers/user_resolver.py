# app/api/graphql/resolvers/user_resolver.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import user as crud_user
from app.db.model import User as UserModel, UserRole as UserRoleModel
from app.api.graphql.schemas.types import User, UserRole

class UserResolver:
    @staticmethod
    def get_all_users(db: Session, role: Optional[UserRole] = None, limit: Optional[int] = None) -> List[User]:
        """Obtener todos los usuarios con filtros opcionales"""
        users = crud_user.get_all_users(db)
        
        # Filtrar por rol si se especifica
        if role:
            users = [user for user in users if user.role == role.value]
        
        # Limitar resultados si se especifica
        if limit:
            users = users[:limit]
        
        # Convertir a tipos GraphQL
        return [
            User(
                id=user.id,
                name=user.name,
                email=user.email,
                role=UserRole(user.role)
            )
            for user in users
        ]
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        user = crud_user.get_user_by_id(db, user_id)
        if not user:
            return None
        
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            role=UserRole(user.role)
        )
    
    @staticmethod
    def get_users_by_role(db: Session, role: UserRole) -> List[User]:
        """Obtener usuarios por rol específico"""
        users = crud_user.get_all_users(db)
        filtered_users = [user for user in users if user.role == role.value]
        
        return [
            User(
                id=user.id,
                name=user.name,
                email=user.email,
                role=UserRole(user.role)
            )
            for user in filtered_users
        ]
    
    @staticmethod
    def get_users_by_email_domain(db: Session, domain: str) -> List[User]:
        """Obtener usuarios por dominio de email"""
        users = crud_user.get_all_users(db)
        filtered_users = [user for user in users if user.email.endswith(domain)]
        
        return [
            User(
                id=user.id,
                name=user.name,
                email=user.email,
                role=UserRole(user.role)
            )
            for user in filtered_users
        ]