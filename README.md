# Microservicio de Notificaciones - UnxChange v1.1.0

Este microservicio maneja el envío de notificaciones por correo electrónico para la plataforma UnxChange, con soporte completo para **API REST** y **GraphQL**.

## 🚀 Funcionalidades


- Envío de correos de confirmación cuando se crea un usuario nuevo
- Envío de correos de confirmación cuando un usuario elige una convocatoria
- Envío de correos masivos a usuarios registrados con filtros avanzados
- Soporte para correos HTML y texto plano
- Logging de todas las operaciones de email
- **API REST** para integración con otros microservicios
- **API GraphQL** con queries flexibles y operaciones combinadas
- **GraphQL Playground** interactivo para desarrollo
- Estadísticas y métricas en tiempo real
- Validación previa de envíos masivos

## 🛠 Tecnologías

- FastAPI como framework web principal
- **Strawberry GraphQL** para API GraphQL moderna
- SQLAlchemy para acceso a PostgreSQL
- PostgreSQL como base de datos principal
- SMTP (Gmail) para envío de correos
- Pydantic para validación de datos
- Prometheus para métricas y monitoreo
- Python 3.12+

## 📋 APIs Disponibles

### 🔗 Endpoints Principales

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Información del servicio y endpoints disponibles |
| `GET /docs` | Documentación interactiva REST API (Swagger) |
| `GET /graphql` | GraphQL Playground interactivo |
| `POST /graphql` | Endpoint GraphQL principal |
| `GET /metrics` | Métricas Prometheus |

---

## 🚀 API REST (v1)

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

Recibe notificaciones cuando un usuario elige una convocatoria.

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

---

## ⚡ API GraphQL

### Acceso al GraphQL Playground

Visita `http://localhost:8002/graphql` para acceder al playground interactivo donde puedes:
- Explorar el schema completo
- Probar queries y mutations en tiempo real
- Ver documentación automática
- Usar autocompletado inteligente

### 🔍 Queries Disponibles

#### Obtener usuarios con filtros
```graphql
query {
  users(role: ESTUDIANTE, limit: 10) {
    id
    name
    email
    role
  }
}
```

#### Obtener usuario específico
```graphql
query {
  user(id: 123) {
    name
    email
    role
  }
}
```

#### Obtener estadísticas de notificaciones
```graphql
query {
  notificationStats {
    totalUsers
    emailsSentToday
    successRate
    totalEmailsSent
  }
}
```

#### Validar envío masivo antes de ejecutar
```graphql
query {
  validateBulkEmail(filters: {
    roles: [ESTUDIANTE, PROFESIONAL]
    emailDomains: ["@unisabana.edu.co"]
  }) {
    recipientCount
    estimatedDeliveryTime
    warnings
    recipientPreview {
      name
      email
    }
  }
}
```

### 🚀 Mutations Disponibles

#### Enviar correo de bienvenida
```graphql
mutation {
  sendWelcomeEmail(input: {
    name: "Juan Pérez"
    email: "juan@example.com"
  }) {
    success
    message
    timestamp
  }
}
```

#### Envío masivo con filtros avanzados
```graphql
mutation {
  sendBulkEmail(input: {
    subject: "Nueva convocatoria disponible"
    content: "Estimado estudiante, hay una nueva convocatoria..."
    filters: {
      roles: [ESTUDIANTE]
      emailDomains: ["@unisabana.edu.co"]
      excludeIds: [1, 2, 3]
    }
  }) {
    success
    message
    totalSent
    failedEmails
  }
}
```

#### Crear usuario y enviar bienvenida automáticamente
```graphql
mutation {
  createUserWithWelcome(input: {
    name: "Ana Martínez"
    email: "ana@example.com" 
    role: ESTUDIANTE
    password: "securepassword"
  }) {
    user {
      id
      name
      email
      role
    }
    welcomeEmail {
      success
      message
    }
    totalUsers
  }
}
```

### 🎯 Ventajas de GraphQL vs REST

| Característica | REST | GraphQL |
|----------------|------|---------|
| **Consultas flexibles** | ❌ Datos fijos | ✅ Solo datos necesarios |
| **Múltiples operaciones** | ❌ Múltiples requests | ✅ Una sola request |
| **Tipado fuerte** | ❌ Manual | ✅ Automático |
| **Documentación** | ❌ Externa | ✅ Auto-generada |
| **Filtros avanzados** | ❌ Limitados | ✅ Flexibles |
| **Validación** | ❌ Manual | ✅ Automática |

---

## ⚙️ Configuración e Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` con:

```env
DATABASE_URL=postgresql://user:password@localhost/notifications_db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-password
JWT_SECRET_KEY=your-secret-key
```

### 3. Ejecutar la aplicación

```bash
uvicorn main:app --reload --port 8002
```

### 4. Acceder a las interfaces

- **API REST Docs**: http://localhost:8002/docs
- **GraphQL Playground**: http://localhost:8002/graphql
- **Métricas**: http://localhost:8002/metrics
- **Servicio Info**: http://localhost:8002/

---

## 🔧 Estructura de Archivos

```plaintext
backend-notifications/
├── main.py                          # Aplicación FastAPI principal
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo
├── CHANGELOG.md                     # Historial de cambios
├── app/
│   ├── api/
│   │   ├── v1/                      # API REST v1
│   │   │   ├── endpoints/
│   │   │   │   └── notification.py  # Endpoints REST
│   │   │   └── schemas.py           # Esquemas Pydantic REST
│   │   └── graphql/                 # API GraphQL ✨ NUEVO
│   │       ├── schema.py            # Schema GraphQL principal  
│   │       ├── router.py            # Router GraphQL
│   │       ├── schemas/
│   │       │   ├── types.py         # Tipos GraphQL
│   │       │   ├── queries.py       # Queries GraphQL
│   │       │   └── mutations.py     # Mutations GraphQL
│   │       └── resolvers/
│   │           ├── user_resolver.py      # Resolvers de usuarios
│   │           └── notification_resolver.py # Resolvers de notificaciones
│   ├── core/
│   │   ├── config.py                # Configuración
│   │   └── email.py                 # Funciones de email
│   ├── crud/
│   │   └── user.py                  # Operaciones CRUD
│   ├── db/
│   │   ├── model.py                 # Modelos SQLAlchemy
│   │   └── session.py               # Sesión de base de datos
│   └── metrics/
│       └── prometheus.py            # Métricas Prometheus
```

---

## 🧪 Ejemplos de Uso

### Caso de Uso 1: Dashboard de Administrador

**Con REST (4 requests):**
```bash
curl GET /api/v1/notification/users/
curl GET /api/v1/notification/stats/     # No implementado
curl GET /api/v1/notification/recent/    # No implementado  
curl GET /api/v1/notification/metrics/   # No implementado
```

**Con GraphQL (1 request):**
```graphql
query DashboardData {
  users(limit: 10) { id name email role }
  notificationStats { totalUsers emailsSentToday successRate }
  recentNotifications(limit: 5) { type recipient sentAt status }
}
```

### Caso de Uso 2: Envío Masivo Inteligente

**GraphQL permite filtros avanzados que REST no tiene:**
```graphql
mutation {
  sendBulkEmail(input: {
    subject: "Nueva convocatoria disponible"
    content: "Estimados estudiantes..."
    filters: {
      roles: [ESTUDIANTE]
      emailDomains: ["@unisabana.edu.co", "@unal.edu.co"] 
      excludeIds: [1, 2, 3]  # Usuarios que ya aplicaron
    }
  }) {
    success
    totalSent
    failedEmails
    message
  }
}
```

---

## 🔄 Migración de REST a GraphQL

Si ya usas la API REST, **no necesitas cambiar nada**. GraphQL es complementario:

- ✅ **REST API sigue funcionando igual**
- ✅ **Misma lógica de negocio**  
- ✅ **Misma base de datos**
- ✅ **Sin breaking changes**

**Recomendación:** Usa GraphQL para nuevas features y operaciones complejas.

---

## 📈 Métricas y Monitoreo

- **Prometheus metrics**: `/metrics`
- **Health check**: `/`
- **API docs**: `/docs`
- **GraphQL introspection**: Habilitado en desarrollo

---

## 🛠 Desarrollo

### Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

### Desarrollo con GraphQL

1. Inicia el servidor: `uvicorn main:app --reload --port 8002`
2. Ve a http://localhost:8002/graphql
3. Explora el schema y prueba queries/mutations
4. La documentación se genera automáticamente

---

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT.
