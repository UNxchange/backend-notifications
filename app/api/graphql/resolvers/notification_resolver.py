# app/api/graphql/resolvers/notification_resolver.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import user as crud_user
from app.core.email import enviar_email, enviar_correo_confirmacion, enviar_correo_convocatoria_elegida
from app.api.graphql.schemas.types import (
    NotificationResult, NotificationStats, RecentNotification, 
    ValidationResult, User, UserRole, BulkEmailFilters
)
from app.api.graphql.resolvers.user_resolver import UserResolver

class NotificationResolver:
    @staticmethod
    def send_welcome_email(db: Session, name: str, email: str) -> NotificationResult:
        """Enviar correo de bienvenida"""
        try:
            enviar_correo_confirmacion(email, name)
            return NotificationResult(
                success=True,
                message=f"Correo de bienvenida enviado exitosamente a {email}",
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return NotificationResult(
                success=False,
                message=f"Error al enviar correo de bienvenida: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    @staticmethod
    def send_convocatoria_notification(
        db: Session,
        user_name: str,
        user_email: str,
        convocatoria_titulo: str,
        convocatoria_descripcion: str,
        universidad_destino: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> NotificationResult:
        """Enviar notificación de convocatoria elegida"""
        try:
            enviar_correo_convocatoria_elegida(
                destinatario=user_email,
                nombre_usuario=user_name,
                titulo_convocatoria=convocatoria_titulo,
                descripcion_convocatoria=convocatoria_descripcion,
                universidad_destino=universidad_destino,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            return NotificationResult(
                success=True,
                message=f"Correo de convocatoria enviado exitosamente a {user_email}",
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            return NotificationResult(
                success=False,
                message=f"Error al enviar correo de convocatoria: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    @staticmethod
    def send_bulk_email(
        db: Session, 
        subject: str, 
        content: str, 
        filters: Optional[BulkEmailFilters] = None
    ) -> NotificationResult:
        """Enviar correo masivo con filtros"""
        try:
            # Obtener todos los usuarios
            all_users = crud_user.get_all_users(db)
            target_users = all_users
            
            # Aplicar filtros si existen
            if filters:
                if filters.roles:
                    role_values = [role.value for role in filters.roles]
                    target_users = [user for user in target_users if user.role in role_values]
                
                if filters.email_domains:
                    target_users = [
                        user for user in target_users 
                        if any(user.email.endswith(domain) for domain in filters.email_domains)
                    ]
                
                if filters.exclude_ids:
                    target_users = [user for user in target_users if user.id not in filters.exclude_ids]
            
            # Enviar correos
            failed_emails = []
            sent_count = 0
            
            for user in target_users:
                try:
                    enviar_email(user.email, subject, content)
                    sent_count += 1
                except Exception as e:
                    failed_emails.append(user.email)
            
            return NotificationResult(
                success=len(failed_emails) == 0,
                message=f"Correos enviados: {sent_count}, Fallidos: {len(failed_emails)}",
                timestamp=datetime.now().isoformat(),
                total_sent=sent_count,
                failed_emails=failed_emails
            )
        except Exception as e:
            return NotificationResult(
                success=False,
                message=f"Error en envío masivo: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
    
    @staticmethod
    def get_notification_stats(db: Session) -> NotificationStats:
        """Obtener estadísticas de notificaciones"""
        users = crud_user.get_all_users(db)
        total_users = len(users)
        
        # Simular estadísticas (en producción estas vendrían de logs/metrics)
        return NotificationStats(
            total_users=total_users,
            emails_sent_today=0,  # Placeholder - implementar con logs reales
            success_rate=95.5,    # Placeholder
            total_emails_sent=0,  # Placeholder
            emails_by_type='{"welcome": 0, "convocatoria": 0, "bulk": 0}'  # Placeholder
        )
    
    @staticmethod
    def validate_bulk_email(
        db: Session, 
        filters: Optional[BulkEmailFilters] = None
    ) -> ValidationResult:
        """Validar envío masivo antes de ejecutar"""
        all_users = crud_user.get_all_users(db)
        target_users = all_users
        
        # Aplicar filtros
        if filters:
            if filters.roles:
                role_values = [role.value for role in filters.roles]
                target_users = [user for user in target_users if user.role in role_values]
            
            if filters.email_domains:
                target_users = [
                    user for user in target_users 
                    if any(user.email.endswith(domain) for domain in filters.email_domains)
                ]
            
            if filters.exclude_ids:
                target_users = [user for user in target_users if user.id not in filters.exclude_ids]
        
        # Convertir a tipos GraphQL para preview
        preview_users = [
            User(
                id=user.id,
                name=user.name,
                email=user.email,
                role=UserRole(user.role)
            )
            for user in target_users[:5]  # Solo los primeros 5 para preview
        ]
        
        # Generar warnings
        warnings = []
        if len(target_users) > 100:
            warnings.append("Gran cantidad de destinatarios. Considere envío por lotes.")
        if len(target_users) == 0:
            warnings.append("Los filtros no coinciden con ningún usuario.")
        
        return ValidationResult(
            recipient_count=len(target_users),
            estimated_delivery_time=f"{len(target_users) * 0.1:.1f} segundos",
            warnings=warnings,
            recipient_preview=preview_users
        )
    
    @staticmethod
    def get_recent_notifications(db: Session, limit: int = 10) -> List[RecentNotification]:
        """Obtener notificaciones recientes"""
        # Placeholder - en producción esto vendría de logs/base de datos
        return [
            RecentNotification(
                type="welcome",
                recipient="ejemplo@test.com",
                sent_at=datetime.now().isoformat(),
                status="sent"
            )
        ]