# Ejemplos de GraphQL para el Microservicio de Notificaciones

Este archivo contiene ejemplos prácticos de queries y mutations GraphQL que puedes usar con el microservicio de notificaciones.

## 🔍 Queries (Consultas)

### 1. Obtener todos los usuarios con información básica

```graphql
query GetAllUsers {
  users {
    id
    name
    email
    role
  }
}
```

### 2. Obtener solo estudiantes con límite

```graphql
query GetStudents {
  users(role: ESTUDIANTE, limit: 5) {
    id
    name
    email
  }
}
```

### 3. Obtener usuario específico por ID

```graphql
query GetUserById {
  user(id: 123) {
    id
    name
    email
    role
  }
}
```

### 4. Obtener usuarios por dominio de email

```graphql
query GetUniversityUsers {
  usersByEmailDomain(domain: "@unisabana.edu.co") {
    id
    name
    email
    role
  }
}
```

### 5. Obtener estadísticas del sistema

```graphql
query GetStats {
  notificationStats {
    totalUsers
    emailsSentToday
    successRate
    totalEmailsSent
    emailsByType
  }
}
```

### 6. Validar envío masivo antes de ejecutar

```graphql
query ValidateBulkEmail {
  validateBulkEmail(filters: {
    roles: [ESTUDIANTE, PROFESIONAL]
    emailDomains: ["@unisabana.edu.co"]
    excludeIds: [1, 2, 3]
  }) {
    recipientCount
    estimatedDeliveryTime
    warnings
    recipientPreview {
      id
      name
      email
    }
  }
}
```

### 7. Obtener notificaciones recientes

```graphql
query GetRecentNotifications {
  recentNotifications(limit: 3) {
    type
    recipient
    sentAt
    status
  }
}
```

### 8. Consulta completa para dashboard de administrador

```graphql
query AdminDashboard {
  # Usuarios recientes
  users(limit: 5) {
    id
    name
    email
    role
  }
  
  # Estadísticas generales
  notificationStats {
    totalUsers
    emailsSentToday
    successRate
  }
  
  # Actividad reciente
  recentNotifications(limit: 3) {
    type
    recipient
    sentAt
    status
  }
}
```

## 🚀 Mutations (Mutaciones)

### 1. Enviar correo de bienvenida

```graphql
mutation SendWelcome {
  sendWelcomeEmail(input: {
    name: "Juan Pérez"
    email: "juan.perez@example.com"
  }) {
    success
    message
    timestamp
  }
}
```

### 2. Enviar notificación de convocatoria

```graphql
mutation SendConvocatoriaNotification {
  sendConvocatoriaNotification(input: {
    userName: "María García"
    userEmail: "maria@unisabana.edu.co"
    convocatoriaTitulo: "Intercambio - Universidad de Barcelona"
    convocatoriaDescripcion: "Programa de intercambio académico semestral"
    universidadDestino: "Universidad de Barcelona"
    fechaInicio: "01/09/2025"
    fechaFin: "31/01/2026"
  }) {
    success
    message
    timestamp
  }
}
```

### 3. Envío masivo básico (a todos los usuarios)

```graphql
mutation SendBulkBasic {
  sendBulkEmail(input: {
    subject: "Anuncio importante"
    content: "Estimados usuarios, queremos informarles sobre..."
  }) {
    success
    message
    totalSent
    failedEmails
    timestamp
  }
}
```

### 4. Envío masivo con filtros avanzados

```graphql
mutation SendBulkFiltered {
  sendBulkEmail(input: {
    subject: "Nueva convocatoria para estudiantes"
    content: "Estimados estudiantes, hay una nueva convocatoria disponible..."
    filters: {
      roles: [ESTUDIANTE]
      emailDomains: ["@unisabana.edu.co", "@unal.edu.co"]
      excludeIds: [1, 5, 10]
    }
  }) {
    success
    message
    totalSent
    failedEmails
    timestamp
  }
}
```

### 5. Crear usuario y enviar bienvenida automáticamente

```graphql
mutation CreateUserWithWelcome {
  createUserWithWelcome(input: {
    name: "Ana Martínez"
    email: "ana.martinez@unisabana.edu.co"
    role: ESTUDIANTE
    password: "securePassword123"
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
      timestamp
    }
    totalUsers
  }
}
```

## 🎯 Casos de Uso Complejos

### Caso 1: Workflow completo de registro de usuario

```graphql
# Paso 1: Validar que el email no esté duplicado
query CheckUserExists {
  usersByEmailDomain(domain: "@unisabana.edu.co") {
    email
  }
}

# Paso 2: Crear usuario y enviar bienvenida
mutation CompleteRegistration {
  createUserWithWelcome(input: {
    name: "Nuevo Usuario"
    email: "nuevo@unisabana.edu.co"
    role: ESTUDIANTE
    password: "password123"
  }) {
    user {
      id
      name
      email
    }
    welcomeEmail {
      success
      message
    }
    totalUsers
  }
}
```

### Caso 2: Campaña de email segmentada

```graphql
# Paso 1: Validar destinatarios
query ValidateStudentCampaign {
  validateBulkEmail(filters: {
    roles: [ESTUDIANTE]
    emailDomains: ["@unisabana.edu.co"]
  }) {
    recipientCount
    warnings
    recipientPreview {
      name
      email
    }
  }
}

# Paso 2: Ejecutar campaña si todo está bien
mutation ExecuteStudentCampaign {
  sendBulkEmail(input: {
    subject: "Nueva oportunidad de intercambio académico"
    content: "Estimados estudiantes, tenemos excelentes noticias..."
    filters: {
      roles: [ESTUDIANTE]
      emailDomains: ["@unisabana.edu.co"]
    }
  }) {
    success
    totalSent
    failedEmails
    message
  }
}
```

### Caso 3: Monitoreo en tiempo real

```graphql
# Query para dashboard en tiempo real
query RealtimeDashboard {
  # Estadísticas actuales
  notificationStats {
    totalUsers
    emailsSentToday
    successRate
    totalEmailsSent
  }
  
  # Actividad reciente
  recentNotifications(limit: 10) {
    type
    recipient
    sentAt
    status
  }
  
  # Usuarios por rol
  studentCount: users(role: ESTUDIANTE) {
    id
  }
  
  professionalCount: users(role: PROFESIONAL) {
    id
  }
  
  adminCount: users(role: ADMINISTRADOR) {
    id
  }
}
```

## 🔧 Tips para usar GraphQL

### 1. Usa aliases para múltiples consultas del mismo tipo

```graphql
query MultipleUserGroups {
  students: users(role: ESTUDIANTE, limit: 5) {
    id
    name
    email
  }
  
  professionals: users(role: PROFESIONAL, limit: 5) {
    id
    name
    email
  }
  
  admins: users(role: ADMINISTRADOR) {
    id
    name
    email
  }
}
```

### 2. Usa fragmentos para reutilizar campos

```graphql
fragment UserInfo on User {
  id
  name
  email
  role
}

query GetUsersWithFragment {
  users(limit: 10) {
    ...UserInfo
  }
  
  user(id: 123) {
    ...UserInfo
  }
}
```

### 3. Combina múltiples operaciones

```graphql
query CombinedOperations {
  # Datos de usuarios
  allUsers: users {
    id
    name
    email
  }
  
  # Estadísticas
  stats: notificationStats {
    totalUsers
    successRate
  }
  
  # Validación de campaña
  validation: validateBulkEmail(filters: {
    roles: [ESTUDIANTE]
  }) {
    recipientCount
    warnings
  }
}
```

## 🚀 Ventajas de estos ejemplos

- **Flexibilidad**: Obtén exactamente los datos que necesitas
- **Eficiencia**: Una sola request para múltiples operaciones  
- **Tipado**: Validación automática en tiempo de desarrollo
- **Documentación**: Schema auto-documentado en GraphQL Playground
- **Filtros avanzados**: Capacidades que no están disponibles en REST
