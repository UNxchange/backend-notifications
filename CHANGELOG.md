# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-13

### Agregado

- **Servicio de notificaciones inicial** para la plataforma UnxChange
- **Endpoint de notificación de usuario creado** (`POST /api/v1/notification/usuario-creado/`)
  - Recibe datos del usuario recién registrado
  - Envía correo de confirmación de registro
  - Integración con microservicio de autenticación
- **Endpoint de notificación de convocatoria elegida** (`POST /api/v1/notification/convocatoria-elegida/`)
  - Recibe datos cuando un usuario selecciona una convocatoria
  - Envía correo de confirmación con detalles de la convocatoria
  - Integración con microservicio de convocatorias
- **Endpoint de envío masivo de correos** (`POST /api/v1/notification/enviar-correo/`)
  - Permite enviar correos a todos los usuarios registrados
  - Funcionalidad de comunicación masiva
- **Endpoint de consulta de usuarios** (`GET /api/v1/notification/users/`)
  - Obtiene lista de todos los usuarios registrados
  - Útil para administración y debugging
- **Sistema de envío de emails HTML**
  - Soporte para correos con formato HTML
  - Templates personalizados para diferentes tipos de notificación
  - Configuración SMTP con Gmail
- **Integración con base de datos PostgreSQL**
  - Modelos SQLAlchemy para gestión de datos
  - Operaciones CRUD para usuarios
  - Sesiones de base de datos optimizadas
- **Arquitectura de microservicio**
  - FastAPI como framework principal
  - Estructura modular con separación de responsabilidades
  - Configuración CORS para integración con frontend
- **Sistema de logging y manejo de errores**
  - Logging de todas las operaciones de email
  - Manejo robusto de excepciones
  - Respuestas HTTP apropiadas para diferentes escenarios
- **Esquemas Pydantic**
  - Validación de datos de entrada
  - Serialización consistente de respuestas
  - Documentación automática de API
- **Configuración de despliegue**
  - Archivo Procfile para Heroku
  - Requirements.txt con todas las dependencias
  - Configuración de variables de entorno

### Tecnologías utilizadas

- FastAPI 0.110.0
- SQLAlchemy 2.0.25
- PostgreSQL con psycopg2-binary 2.9.9
- Pydantic 2.5.3 con soporte para validación de email
- Python 3.12+
- Uvicorn para servidor ASGI
- SMTP para envío de emails

### Funcionalidades principales

- ✅ Notificaciones de registro de usuario
- ✅ Notificaciones de selección de convocatoria
- ✅ Envío masivo de correos
- ✅ Gestión de usuarios
- ✅ Integración con otros microservicios
- ✅ API REST completa
- ✅ Documentación automática con FastAPI

### Seguridad

- Validación de datos con Pydantic
- Manejo seguro de credenciales SMTP
- CORS configurado para producción

### Documentación

- README.md con paso a paso de como usar el microservicio
- Documentación automática de API disponible en `/docs`
- Esquemas de request/response documentados

---

## Notas de desarrollo

- **Estructura del proyecto**: Sigue las mejores prácticas de FastAPI con separación clara entre API, lógica de negocio y acceso a datos
- **Testing**: Configurado con pytest para testing asyncrono
- **Logging**: Implementado para todas las operaciones críticas
- **Escalabilidad**: Diseñado para manejar múltiples tipos de notificaciones y integración con diferentes microservicios
