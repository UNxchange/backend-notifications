# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import notification
from app.api.graphql.router import graphql_router

#metrics
from app.metrics.prometheus import prometheus_middleware, prometheus_metrics

# Importar el consumidor de RabbitMQ
from app.broker import start_consumer
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notification Service",
    version="1.2.0",
    description="Microservicio de notificaciones con API REST, GraphQL y RabbitMQ Consumer"
)


# Agregar el middleware
app.middleware("http")(prometheus_middleware)

# Incluir routers
app.include_router(notification.router, prefix="/api/v1/notification", tags=["Notification"])
app.include_router(graphql_router, prefix="/api/v1/notification/graphql", tags=["GraphQL"])

# Configuración CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8001",
    ],  # Orígenes específicos en lugar de "*"
    allow_credentials=True,  # Permitir credenciales
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Evento de inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    """Inicia el consumidor de RabbitMQ al arrancar la aplicación"""
    try:
        logger.info("🚀 Iniciando consumidor de RabbitMQ...")
        start_consumer()
        logger.info("✅ Consumidor de RabbitMQ iniciado exitosamente")
    except Exception as e:
        logger.error(f"❌ Error iniciando consumidor de RabbitMQ: {e}")


# Endpoint de bienvenida o de health check
@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "ok", 
        "service": "unxchange-notification-service",
        "version": "1.2.0",
        "features": ["REST API", "GraphQL", "RabbitMQ Consumer"],
        "endpoints": {
            "rest_api": "/api/v1/notification/",
            "graphql": "/api/v1/notification/graphql",
            "graphql_playground": "/api/v1/notification/graphql (GET)",
            "docs": "/docs",
            "metrics": "/metrics"
        }
    }

# Endpoint para Prometheus
@app.get("/metrics")
def metrics():
    return prometheus_metrics()