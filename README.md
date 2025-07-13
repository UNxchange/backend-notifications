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

2. Ejecutar la aplicación:

```bash
uvicorn main:app --reload --port 8002
```

## 🔧 Estructura de archivos

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

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT.
