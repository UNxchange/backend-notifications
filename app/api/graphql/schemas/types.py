# app/api/graphql/schemas/types.py
import strawberry
from strawberry.scalars import JSON
from enum import Enum
from typing import List, Optional
from datetime import datetime

@strawberry.enum
class UserRole(Enum):
    ESTUDIANTE = "estudiante"
    PROFESIONAL = "profesional" 
    ADMINISTRADOR = "administrador"

@strawberry.type
class User:
    id: int
    name: str
    email: str
    role: UserRole

@strawberry.type
class Notification:
    id: int
    user_id: int
    type: str
    title: str
    message: str
    is_read: bool
    created_at: str
    read_at: Optional[str] = None
    metadata: Optional[JSON] = None
    user: Optional[User] = None

@strawberry.input
class NotificationInput:
    user_id: int
    type: str
    title: str
    message: str
    metadata: Optional[JSON] = None

@strawberry.type
class NotificationResult:
    success: bool
    message: str
    timestamp: str
    total_sent: Optional[int] = None
    failed_emails: Optional[List[str]] = None

@strawberry.type
class NotificationStats:
    total_users: int
    emails_sent_today: int
    success_rate: float
    total_emails_sent: int
    emails_by_type: Optional[str] = None  # JSON string

@strawberry.type
class RecentNotification:
    type: str
    recipient: str
    sent_at: str
    status: str

@strawberry.type
class ValidationResult:
    recipient_count: int
    estimated_delivery_time: str
    warnings: List[str]
    recipient_preview: List[User]

@strawberry.input
class WelcomeEmailInput:
    name: str
    email: str

@strawberry.input
class ConvocatoriaInput:
    user_name: str
    user_email: str
    convocatoria_titulo: str
    convocatoria_descripcion: str
    universidad_destino: str
    fecha_inicio: str
    fecha_fin: str

@strawberry.input
class BulkEmailFilters:
    roles: Optional[List[UserRole]] = None
    email_domains: Optional[List[str]] = None
    exclude_ids: Optional[List[int]] = None

@strawberry.input
class BulkEmailInput:
    subject: str
    content: str
    filters: Optional[BulkEmailFilters] = None

@strawberry.input
class UserInput:
    id: Optional[int] = None  # ID opcional del usuario (si ya fue creado)
    name: str
    email: str
    role: UserRole
    password: Optional[str] = None  # Password opcional (no necesario para notificaciones)

@strawberry.type
class UserWithNotification:
    user: User
    welcome_email: NotificationResult
    total_users: int