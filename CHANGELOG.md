# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-14

### Agregado

- **Microservicio de notificaciones inicial** para la plataforma UnxChange
- **Envío de correos electrónicos** mediante Gmail SMTP
  - Soporte para correos de bienvenida a nuevos usuarios
  - Confirmación de postulación a convocatorias
  - Plantillas en texto plano y HTML
- **API REST para notificaciones**
  - `POST /api/v1/usuario-creado/` para notificar creación de usuario y enviar correo de bienvenida
  - `POST /api/v1/convocatoria-elegida/` para notificar postulación a convocatoria y enviar confirmación
  - `POST /api/v1/enviar-correo/` para envío masivo de correos a todos los usuarios
  - `GET /api/v1/users/` para listar usuarios registrados
- **Base de datos PostgreSQL**
  - Modelo de usuario con roles y autenticación básica
  - Integración con SQLAlchemy ORM
- **Arquitectura de microservicio FastAPI**
  - API REST con documentación automática (`/docs`)
  - Estructura modular y separación de responsabilidades
- **Sistema de métricas Prometheus**
  - Middleware para instrumentar métricas de uso, latencia y errores
  - Endpoint `/metrics` para monitoreo y observabilidad
- **Configuración de despliegue**
  - Variables de entorno para conexión a base de datos, correo y JWT
  - Ejemplo de archivo `.env`
  - Soporte para ejecución local con Uvicorn

### Tecnologías utilizadas

- FastAPI como framework web principal
- SQLAlchemy para acceso a PostgreSQL
- Pydantic para validación y serialización de datos
- Prometheus Client para métricas
- Python 3.12+
- Uvicorn para servidor ASGI

### Funcionalidades principales

- ✅ Envío de correos de bienvenida y confirmación de postulación
- ✅ API REST para integración con otros microservicios
- ✅ Gestión de usuarios y roles
- ✅ Métricas Prometheus para monitoreo
- ✅ Configuración segura mediante variables de entorno

### Seguridad

- Validación de datos de entrada con Pydantic
- Variables de entorno para credenciales sensibles
- Manejo de errores y respuestas HTTP adecuadas

### Arquitectura

- **Endpoints**: `/api/v1/usuario-creado/`, `/api/v1/convocatoria-elegida/`, `/api/v1/enviar-correo/`, `/api/v1/users/`
- **Modelos**: Usuario con campos de nombre, email, rol y contraseña
- **Core**: Configuración, envío de correos y métricas
- **Schemas**: Validación y serialización de datos

### Integración

- **Microservicio de autenticación**: Recibe notificaciones de usuarios creados
- **Microservicio de convocatorias**: Recibe notificaciones de postulaciones
- **Frontend**: API REST documentada
- **Base de datos**: PostgreSQL
- **Despliegue**: Uvicorn y variables de entorno

---

## Documentación técnica

### Endpoints disponibles

- `POST /api/v1/usuario-creado/` - Notificar creación de usuario y enviar correo de bienvenida
- `POST /api/v1/convocatoria-elegida/` - Notificar postulación y enviar correo de confirmación
- `POST /api/v1/enviar-correo/` - Enviar correo masivo a todos los usuarios
- `GET /api/v1/users/` - Listar usuarios registrados

### Modelos de datos

- **User**: Modelo principal con id, name, email, role, hashed_password
- **UserCreatedNotification**: Schema para notificación de usuario creado
- **ConvocatoriaElegidaNotification**: Schema para notificación de postulación a convocatoria

---

## Notas de desarrollo

- **Pruebas**: Agregar tests unitarios y de integración en futuras versiones
- **Logs**: Mejorar sistema de logging para auditoría
- **Monitoreo**: Ampliar métricas y alertas
- **Documentación**: La documentación interactiva está
