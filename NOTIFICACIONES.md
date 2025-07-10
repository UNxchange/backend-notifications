# Microservicio de Notificaciones - UnxChange

## Endpoint para Notificación de Usuario Creado

### POST `/api/v1/notification/usuario-creado/`

Este endpoint recibe notificaciones desde el microservicio de autenticación cuando se crea un nuevo usuario y envía automáticamente un correo de confirmación.

#### Request Body

```json
{
  "name": "Juan Pérez",
  "email": "juan.perez@example.com"
}
```

#### Response

**Success (200)**
```json
{
  "success": true,
  "message": "Correo de confirmación enviado exitosamente a juan.perez@example.com"
}
```

**Error (500)**
```json
{
  "detail": "Error al enviar correo de confirmación: [error message]"
}
```

## Integración con el Microservicio de Autenticación

Para integrar este endpoint con el microservicio de autenticación, debes hacer una petición HTTP POST después de crear un usuario:

```python
import requests

def notify_user_created(user_name: str, user_email: str):
    """
    Notifica al microservicio de notificaciones que se creó un nuevo usuario
    """
    notification_service_url = "http://localhost:8002/api/v1/notification/usuario-creado/"
    
    payload = {
        "name": user_name,
        "email": user_email
    }
    
    try:
        response = requests.post(notification_service_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al notificar creación de usuario: {e}")
        return None
```

## Configuración de Email

Asegúrate de configurar las siguientes variables de entorno en tu archivo `.env`:

```env
EMAIL_ADDRESS=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password
```

**Nota**: Para Gmail, necesitas usar una "App Password" en lugar de tu contraseña regular.

## Ejemplo de Correo de Confirmación

El correo que se envía incluye:
- Mensaje de bienvenida personalizado
- Información sobre UnxChange
- Formato HTML atractivo
- Versión en texto plano como respaldo

## Logs

El sistema registra:
- Intentos de envío de correos
- Correos enviados exitosamente
- Errores en el envío
