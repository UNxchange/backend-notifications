# Microservicio de Notificaciones - UnxChange

Este microservicio maneja el envío de notificaciones por correo electrónico para la plataforma UnxChange.

## 🚀 Funcionalidades

- Envío de correos de confirmación cuando se crea un usuario nuevo
- Envío de correos de confirmación cuando un usuario elige una convocatoria
- Envío de correos masivos a usuarios registrados
- Soporte para correos HTML y texto plano
- Logging de todas las operaciones de email
- API REST para integración con otros microservicios

## 🛠 Tecnologías

- FastAPI
- SQLAlchemy
- PostgreSQL
- SMTP (Gmail)
- Pydantic
- Python 3.12+

## 📋 Endpoints Principales

### POST `/api/v1/notification/usuario-creado/`

Recibe notificaciones de usuario creado y envía correo de confirmación.

**Request Body:**

```json
{
  "name": "Juan Pérez",
  "email": "juan.perez@example.com"
}
```

### POST `/api/v1/notification/convocatoria-elegida/`

Recibe notificaciones cuando un usuario elige una convocatoria y envía correo de confirmación.

**Request Body:**

```json
{
  "user_name": "María García",
  "user_email": "maria.garcia@example.com",
  "convocatoria_titulo": "Intercambio Académico - Universidad de Barcelona",
  "convocatoria_descripcion": "Programa de intercambio semestral",
  "universidad_destino": "Universidad de Barcelona",
  "fecha_inicio": "01/09/2025",
  "fecha_fin": "31/01/2026"
}
```

### POST `/api/v1/notification/enviar-correo/`

Envía correos masivos a todos los usuarios registrados.

### GET `/api/v1/notification/users/`

Obtiene lista de todos los usuarios registrados.

## ⚙️ Configuración

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Crear archivo `.env` basado en `env.example`:

```env
DATABASE_URL=postgresql://user:password@localhost/notifications_db
SECRET_KEY=your-secret-key-here
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
LOG_LEVEL=INFO
```

3. Ejecutar la aplicación:

```bash
uvicorn main:app --reload --port 8002
```

## 🔗 Integración con Microservicio de Autenticación

Para integrar con el microservicio de autenticación, utiliza el archivo `notification_client.py` incluido:

```python
from notification_client import send_welcome_email

# Después de crear un usuario exitosamente
send_welcome_email(user.name, user.email)
```

## 📧 Configuración de Email

### Gmail

1. Habilitar verificación en dos pasos
2. Generar una contraseña de aplicación
3. Usar la contraseña de aplicación en `EMAIL_PASSWORD`

### Otros proveedores

Modificar la configuración SMTP en `app/core/email.py`:

```python
# Para otros proveedores
smtp.gmail.com:465  # Gmail
smtp.outlook.com:587  # Outlook
smtp.mail.yahoo.com:465  # Yahoo
```

## 🧪 Testing

Ejecutar pruebas:

```bash
pytest test_notification.py -v
```

## 📝 Logs

Los logs se muestran en consola con información sobre:

- Intentos de envío de correos
- Correos enviados exitosamente
- Errores en el envío

## 🔧 Desarrollo

### Estructura de archivos

```plaintext
app/
├── main.py                 # Aplicación FastAPI
├── api/v1/
│   ├── endpoints/
│   │   └── notification.py # Endpoints de notificación
│   └── schemas.py          # Esquemas Pydantic
├── core/
│   ├── config.py           # Configuración
│   └── email.py            # Funciones de email
├── crud/
│   └── user.py             # Operaciones CRUD
└── db/
    ├── model.py            # Modelos SQLAlchemy
    └── session.py          # Sesión de base de datos
```

### Agregar nuevos tipos de notificación

1. Crear nuevo schema en `schemas.py`
2. Agregar función de email en `email.py`
3. Crear endpoint en `notification.py`
4. Agregar tests correspondientes

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT.
