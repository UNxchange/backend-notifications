# notification_client.py
"""
Cliente para comunicarse con el microservicio de notificaciones
Este archivo debe ser agregado al microservicio de autenticación
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class NotificationClient:
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url
        self.notification_url = f"{base_url}/api/v1/notification/usuario-creado/"
    
    def notify_user_created(self, user_name: str, user_email: str) -> Optional[dict]:
        """
        Notifica al microservicio de notificaciones que se creó un nuevo usuario
        
        Args:
            user_name: Nombre del usuario creado
            user_email: Email del usuario creado
            
        Returns:
            Respuesta del microservicio de notificaciones o None si hay error
        """
        payload = {
            "name": user_name,
            "email": user_email
        }
        
        try:
            logger.info(f"Notificando creación de usuario: {user_email}")
            
            response = requests.post(
                self.notification_url,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Notificación enviada exitosamente para {user_email}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al notificar creación de usuario {user_email}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al notificar creación de usuario {user_email}: {e}")
            return None

# Instancia global del cliente
notification_client = NotificationClient()

# Función de conveniencia
def send_welcome_email(user_name: str, user_email: str) -> bool:
    """
    Envía un correo de bienvenida a un usuario recién creado
    
    Args:
        user_name: Nombre del usuario
        user_email: Email del usuario
        
    Returns:
        True si se envió exitosamente, False en caso contrario
    """
    result = notification_client.notify_user_created(user_name, user_email)
    return result is not None and result.get("success", False)
